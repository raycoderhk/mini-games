#!/usr/bin/env node
/**
 * Kanban Board Update Checker
 * Compares current kanban-board.json with last checked state
 * Sends Discord notification if changes detected
 * 
 * Usage: node check-kanban-updates.js [--force]
 */

const fs = require('fs');
const path = require('path');

const KANBAN_FILE = path.join(__dirname, '..', 'kanban-board.json');
const STATE_FILE = path.join(__dirname, '..', 'memory', 'kanban-last-checked.json');
const DISCORD_CHANNEL_ID = '1476504735350521958'; // #kanban-updates

// Check if running in OpenClaw environment
const isOpenClaw = process.env.OPENCLAW_WORKSPACE !== undefined;

console.log('🔍 Kanban Board Update Checker');
console.log('================================\n');

// Force check flag
const forceCheck = process.argv.includes('--force');

// Read current kanban data
if (!fs.existsSync(KANBAN_FILE)) {
  console.error('❌ Kanban board file not found:', KANBAN_FILE);
  process.exit(1);
}

const kanbanData = JSON.parse(fs.readFileSync(KANBAN_FILE, 'utf-8'));
const currentUpdated = kanbanData.meta.updated;
const currentProjects = kanbanData.projects || [];

console.log('📊 Current Kanban State:');
console.log(`   Last Updated: ${currentUpdated}`);
console.log(`   Total Projects: ${currentProjects.length}`);

// Read last checked state
let lastState = null;
if (fs.existsSync(STATE_FILE)) {
  lastState = JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
  console.log(`\n📋 Last Checked: ${lastState.lastChecked}`);
  console.log(`   Last Updated (then): ${lastState.lastUpdated}`);
  console.log(`   Project Count (then): ${lastState.projectCount}`);
} else {
  console.log('\n⚠️  No previous state found (first run)');
}

// Check for changes
const hasChanges = forceCheck || !lastState || currentUpdated !== lastState.lastUpdated;

if (!hasChanges) {
  console.log('\n✅ No changes detected');
  console.log('   (Kanban board not updated since last check)');
  process.exit(0);
}

console.log('\n🎉 Changes detected!');

// Analyze changes
const changes = analyzeChanges(lastState, currentProjects);

// Generate notification message
const message = generateNotification(changes, kanbanData);

console.log('\n📝 Notification Message:');
console.log('---');
console.log(message);
console.log('---\n');

// Update state file
const newState = {
  lastChecked: new Date().toISOString(),
  lastUpdated: currentUpdated,
  projectCount: currentProjects.length,
  completedProjects: currentProjects.filter(p => p.status === 'done').length,
  inProgressProjects: currentProjects.filter(p => p.status === 'in_progress').length,
  todoProjects: currentProjects.filter(p => p.status === 'todo').length,
  blockedProjects: currentProjects.filter(p => p.status === 'blocked').length,
  lastChange: changes.summary
};

fs.writeFileSync(STATE_FILE, JSON.stringify(newState, null, 2));
console.log('✅ State file updated');

// Output for OpenClaw to capture
console.log('\n================================');
console.log('OPENCLAW_SIGNAL:KANBAN_UPDATE');
console.log('CHANNEL:' + DISCORD_CHANNEL_ID);
console.log('MESSAGE_START');
console.log(message);
console.log('MESSAGE_END');

// Function to analyze changes
function analyzeChanges(lastState, currentProjects) {
  const changes = {
    newProjects: [],
    completedProjects: [],
    statusChanges: [],
    summary: ''
  };

  if (!lastState) {
    changes.summary = `Initial state: ${currentProjects.length} projects`;
    return changes;
  }

  // Create map of old projects
  const oldProjectsMap = new Map();
  // We don't have old project data, so we'll just detect new ones
  
  // Count by status
  const statusCounts = {
    done: currentProjects.filter(p => p.status === 'done').length,
    in_progress: currentProjects.filter(p => p.status === 'in_progress').length,
    todo: currentProjects.filter(p => p.status === 'todo').length,
    blocked: currentProjects.filter(p => p.status === 'blocked').length
  };

  // Detect changes based on counts
  if (lastState) {
    if (statusCounts.done > lastState.completedProjects) {
      const newlyCompleted = currentProjects.filter(p => 
        p.status === 'done' && 
        new Date(p.completed) > new Date(lastState.lastChecked)
      );
      newlyCompleted.forEach(p => {
        changes.completedProjects.push({
          title: p.title,
          completedAt: p.completed
        });
      });
    }

    if (currentProjects.length > lastState.projectCount) {
      // New projects added (simplified detection)
      changes.newProjects.push({
        count: currentProjects.length - lastState.projectCount
      });
    }

    if (statusCounts.in_progress !== lastState.inProgressProjects ||
        statusCounts.todo !== lastState.todoProjects ||
        statusCounts.blocked !== lastState.blockedProjects) {
      changes.statusChanges.push('Status distribution changed');
    }
  }

  // Generate summary
  const parts = [];
  if (changes.completedProjects.length > 0) {
    parts.push(`${changes.completedProjects.length} completed`);
  }
  if (changes.newProjects.length > 0) {
    parts.push(`${changes.newProjects[0].count} new`);
  }
  if (changes.statusChanges.length > 0) {
    parts.push('status changes');
  }

  changes.summary = parts.length > 0 
    ? parts.join(', ') 
    : 'Metadata updated';

  return changes;
}

// Function to generate Discord notification
function generateNotification(changes, kanbanData) {
  const projects = kanbanData.projects || [];
  
  // Calculate stats
  const stats = {
    total: projects.length,
    done: projects.filter(p => p.status === 'done').length,
    inProgress: projects.filter(p => p.status === 'in_progress').length,
    todo: projects.filter(p => p.status === 'todo').length,
    blocked: projects.filter(p => p.status === 'blocked').length
  };

  // Build message
  let message = '## 📊 Kanban Board Updated\n\n';

  if (changes.completedProjects && changes.completedProjects.length > 0) {
    message += '**✅ Recently Completed:**\n';
    changes.completedProjects.forEach(p => {
      message += `• ${p.title}\n`;
    });
    message += '\n';
  }

  if (changes.newProjects && changes.newProjects.length > 0) {
    message += `**➕ New Projects:** ${changes.newProjects[0].count} added\n\n`;
  }

  if (changes.statusChanges && changes.statusChanges.length > 0) {
    message += '**🔄 Status Changes Detected**\n\n';
  }

  message += '**📈 Current Stats:**\n';
  message += `• Total: ${stats.total} projects\n`;
  message += `• 🔄 In Progress: ${stats.inProgress}\n`;
  message += `• 📝 To Do: ${stats.todo}\n`;
  message += `• ✅ Done: ${stats.done}\n`;
  
  if (stats.blocked > 0) {
    message += `• 🚧 Blocked: ${stats.blocked}\n`;
  }

  // Show recent in-progress items
  const inProgress = projects.filter(p => p.status === 'in_progress');
  if (inProgress.length > 0) {
    message += '\n**🎯 Current Focus:**\n';
    inProgress.slice(0, 3).forEach(p => {
      const priority = p.priority === 'urgent' ? '🔴' : 
                       p.priority === 'high' ? '🟠' : 
                       p.priority === 'medium' ? '🟡' : '🟢';
      message += `${priority} ${p.title}\n`;
    });
  }

  message += '\n---\n*Auto-generated by Kanban Monitor Heartbeat*';

  return message;
}
