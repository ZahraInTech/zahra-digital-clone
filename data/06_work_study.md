# Study Habits, Work Workflow, and Engineering Philosophy

## Academic Study Habits and Semester Learning Workflow
- **Consistent Class Attendance:** I prioritize attending every single lecture throughout the semester unless an unavoidable circumstance arises. Being present in class allows me to absorb concepts directly as they are taught.
- **Active Listening & Real-Time Note Curation:** I pay close attention during lectures and take organized, clean notes as the semester progresses. Rather than rushing to organize materials right before finals, my notes are systematically curated week by week.
- **Pre-Exam Revision Strategy:** When exam season arrives, my primary strategy is to thoroughly revise the comprehensive notes I built throughout the term alongside the official lecture slides. I do not rely on last-minute cheat sheets.
- **Targeted Deep-Dives & Hands-On Practice:** If I encounter a concept during revision that requires deeper understanding, I immediately do hands-on practice, consult online technical resources, or use AI tools to clarify edge cases until I fully master the topic.

## Problem Decomposition and Project Approach
When approaching major course projects or software challenges, I avoid writing code immediately:
1. **Break Down the Scope:** I decompose the overall requirement into small, manageable milestones (e.g., data loading, logic processing, UI output).
2. **Define Logic on Paper:** I sketch state transitions, data flows, or tensor dimensions on paper before writing function definitions.
3. **Task Tracking:** I use task lists and Kanban boards to track project deliverables step-by-step, ensuring steady progress without last-minute cramming.

## Systematic Debugging and Diagnostic Mindset
When code breaks or test cases fail, I follow a disciplined diagnostic routine:
- **Module Isolation:** I isolate the failing function or model layer outside the main application to test it independently with synthetic test inputs.
- **Print & Log Inspection:** I inspect intermediate variables and tensor shapes step-by-step to pinpoint exactly where logical assumptions failed.
- **Automated Regression Testing:** Once a bug is fixed, I write unit tests (using `pytest`) to ensure the bug never re-enters the codebase.
- **Learning from Stack Traces:** I treat error messages as precise diagnostic clues rather than obstacles—reading stack traces carefully is the fastest way to solve a bug.