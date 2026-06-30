# CloudGuard AI - Student 1 Frontend Guide

Role: React dashboard, Tailwind CSS, charts, findings table, AI explanation UI, report download UI, and API integration.

This guide assumes you have never built a software project before. That is okay. Your job is to build the part of CloudGuard AI that users see in the browser.

## 1. Your Role In Simple Words

You are building the dashboard.

The dashboard is like the control room of CloudGuard AI. The backend and security engine find problems, but your frontend helps people understand those problems.

You will build:

- A page where users click "Run Scan"
- Cards that show risk summary
- A security score chart
- A table of security findings
- Filters for severity and cloud service
- A panel that shows AI explanations
- A button to download a PDF report

If the frontend does not exist, the project may still scan resources, but nobody can use it easily during the demo.

## 2. Concepts You Must Understand First

### Website

What it is: A website is a collection of pages opened in a browser.

Why we need it: Users need a visual way to use CloudGuard AI.

Problem it solves: Without a website, users would need to type commands manually.

How it fits: The React app is the CloudGuard AI website.

Analogy: A restaurant kitchen is the backend, but the menu and dining area are the frontend.

If we do not use it: The project becomes difficult to demonstrate.

### Frontend

What it is: The part of an application users see and click.

Why we need it: It makes the project interactive.

Problem it solves: It hides technical backend details from users.

How it fits: Your React app talks to Student 2's FastAPI backend.

Analogy: A car dashboard shows speed, fuel, and warning lights. The engine does the work, but the dashboard helps the driver understand it.

If we do not use it: Reviewers cannot easily see scan results.

### React

What it is: A JavaScript library for building user interfaces.

Why we need it: It lets us build reusable UI pieces called components.

Problem it solves: Large pages become easier to manage.

How it fits: CloudGuard AI dashboard will be built using React components.

Analogy: React components are like Lego blocks. You build small blocks and combine them into a full model.

If we do not use it: You can still use plain HTML, but the dashboard will be harder to organize.

### Tailwind CSS

What it is: A styling tool that lets you design pages using small class names.

Why we need it: It helps make the dashboard look professional quickly.

Problem it solves: Writing large CSS files can be confusing for beginners.

How it fits: You will use Tailwind for cards, buttons, colors, spacing, and responsive design.

Analogy: Tailwind is like ready-made design stickers you apply to HTML elements.

If we do not use it: You must write more CSS manually.

### API

What it is: A way for two programs to talk to each other.

Why we need it: The frontend needs scan data from the backend.

Problem it solves: React cannot directly read the database or scan Localstack.

How it fits: React calls FastAPI endpoints such as `/api/scans`.

Analogy: In a restaurant, the waiter carries orders between the customer and kitchen. The API is the waiter.

If we do not use it: The frontend cannot get real scan results.

### JSON

What it is: A simple text format for sending data.

Why we need it: APIs commonly send data as JSON.

Problem it solves: It gives frontend and backend a shared data format.

How it fits: Student 2's backend sends findings to your React app as JSON.

Analogy: JSON is like a neatly filled form with labels and values.

If we do not use it: Frontend and backend may not understand each other.

Example:

```json
{
  "score": 72,
  "total_findings": 5,
  "critical_count": 1
}
```

## 3. Installations

### Install Visual Studio Code

Website: `https://code.visualstudio.com/`

What to click:

1. Open the website.
2. Click "Download for Windows".
3. Run the installer.
4. Keep default options.
5. Select "Add to PATH" if shown.

Version: Latest stable version.

How to verify:

Open PowerShell and run:

```powershell
code --version
```

Command explanation:

- What it does: Shows the installed VS Code version.
- Why we run it: To check that VS Code installed correctly.
- Expected output: A version number such as `1.xx.x`.
- Common error: `code is not recognized`.
- Fix: Restart the computer or reinstall VS Code with "Add to PATH" enabled.

### Install Node.js

Website: `https://nodejs.org/`

What to click:

1. Open the website.
2. Download the LTS version.
3. Run the installer.
4. Keep default options.
5. Make sure npm is included.

Version: LTS version, not Current.

How to verify:

```powershell
node --version
```

Command explanation:

- What it does: Shows the installed Node.js version.
- Why we run it: React needs Node.js to run development tools.
- Expected output: Something like `v20.x.x` or newer.
- Common error: `node is not recognized`.
- Fix: Restart PowerShell or reinstall Node.js.

```powershell
npm --version
```

Command explanation:

- What it does: Shows the npm version.
- Why we run it: npm installs frontend packages.
- Expected output: A number such as `10.x.x`.
- Common error: `npm is not recognized`.
- Fix: Reinstall Node.js LTS.

### Install Git

Website: `https://git-scm.com/downloads`

What to click:

1. Click Windows.
2. Download 64-bit Git for Windows.
3. Run installer.
4. Keep default options.
5. Choose "Git from the command line" if asked.

How to verify:

```powershell
git --version
```

Command explanation:

- What it does: Shows installed Git version.
- Why we run it: The team will share code using GitHub.
- Expected output: `git version 2.x.x`.
- Common error: `git is not recognized`.
- Fix: Restart PowerShell or reinstall Git.

## 4. Frontend Folder Structure

You will mainly work inside:

```text
frontend/
  src/
    api/
      client.js
      scans.js
      findings.js
      reports.js
    pages/
      Dashboard.jsx
      ScanDetails.jsx
    components/
      Layout.jsx
      SecurityScoreCard.jsx
      RiskSummaryCards.jsx
      FindingsTable.jsx
      FiltersBar.jsx
      AIExplanationPanel.jsx
      ReportDownloadButton.jsx
      SeverityBadge.jsx
      ServiceBadge.jsx
      LoadingState.jsx
      ErrorState.jsx
    lib/
      formatters.js
      severity.js
```

What this means:

- `api/` contains code that talks to the backend.
- `pages/` contains full screens.
- `components/` contains small reusable UI parts.
- `lib/` contains helper functions.

Analogy: A college project file has sections. The frontend folder is also divided into sections so it stays clean.

## 5. APIs Student 2 Will Provide

Student 2 builds the backend. Your frontend will call these APIs:

| API | What it gives you |
|---|---|
| `GET /api/health` | Checks if backend is alive |
| `POST /api/scans` | Starts a scan |
| `GET /api/scans/latest` | Gets latest scan summary |
| `GET /api/scans/{scan_id}/findings` | Gets findings for one scan |
| `POST /api/findings/{finding_id}/explain` | Gets AI explanation |
| `GET /api/reports/{scan_id}/pdf` | Downloads PDF report |

## 6. What Student 3 Is Building

Student 3 builds:

- Security rules
- Risk scoring
- Groq AI explanation logic
- PDF generation

How this affects you:

- You display Student 3's findings in a table.
- You show the score calculated by Student 3.
- You show AI explanations generated by Student 3.
- You download the PDF generated by Student 3's module through Student 2's API.

## 7. Data You Will Receive

Scan response:

```json
{
  "scan_id": "abc-123",
  "status": "completed",
  "score": 42,
  "summary": {
    "total": 7,
    "critical": 2,
    "high": 3,
    "medium": 2,
    "low": 0
  }
}
```

Finding response:

```json
{
  "id": "finding-1",
  "service": "EC2",
  "resource_id": "sg-12345",
  "title": "Security group allows SSH from the internet",
  "severity": "HIGH",
  "description": "Port 22 is open to 0.0.0.0/0",
  "has_ai_explanation": false
}
```

AI explanation response:

```json
{
  "explanation": "This security group allows SSH access from anywhere.",
  "danger": "Attackers can try to log in from the internet.",
  "real_world_impact": "A compromised server can expose data.",
  "remediation_steps": [
    "Open the security group settings.",
    "Remove access from 0.0.0.0/0.",
    "Allow only trusted IP addresses."
  ],
  "estimated_effort": "Easy (5 minutes)"
}
```

## 8. Beginner React Architecture

Use this simple flow:

```text
Dashboard.jsx
  calls API functions
  stores data in state
  passes data to components

Components
  display data
  send button clicks back to Dashboard
```

Do not add Redux in MVP. React state is enough.

Why: Redux is useful for large apps, but it adds extra learning. For CloudGuard AI, one main dashboard is enough.

## 9. Useful Commands

### Create React App With Vite

```powershell
npm create vite@latest frontend -- --template react
```

Command explanation:

- What it does: Creates a new React project in a folder named `frontend`.
- Why we run it: We need a starting React project.
- Expected output: npm asks for confirmation and creates files.
- Common error: Internet or npm error.
- Fix: Check internet, run PowerShell as normal user, retry.

### Install Frontend Packages

```powershell
npm install
```

Command explanation:

- What it does: Installs packages listed in `package.json`.
- Why we run it: React needs these packages to run.
- Expected output: A `node_modules` folder appears.
- Common error: Permission error or network error.
- Fix: Close VS Code terminals and retry. Check internet.

```powershell
npm install axios recharts lucide-react react-hot-toast
```

Command explanation:

- What it does: Installs API, chart, icon, and toast libraries.
- Why we run it: These help build the dashboard faster.
- Expected output: Package names appear in `package.json`.
- Common error: Package install fails.
- Fix: Check spelling and internet connection.

### Start Frontend

```powershell
npm run dev
```

Command explanation:

- What it does: Starts the React development server.
- Why we run it: To view the dashboard in the browser.
- Expected output: A local URL such as `http://localhost:5173`.
- Common error: Port already in use.
- Fix: Stop the old terminal or use the new port shown by Vite.

## 10. Day-By-Day Roadmap

### Week 1

Main objective: Set up the frontend project, understand the basic React building blocks, and make the first dashboard skeleton that can talk to the backend.

By the end of the week: The `frontend` app should run locally, the folder structure should make sense, the first reusable components should exist, the dashboard should look cleaner with Tailwind CSS, and the app should be able to check whether the backend is online.

Day 1: Install the tools, create the React project, and prove the app runs

Today's goal: get the computer ready for frontend work and start a real React project.

Simple language:

- `VS Code` is the editor where you write code.
- The `terminal` is where you type commands.
- `Node.js` lets React tools run on your computer.
- `Git` helps the team save and share code.

Step-by-step:

1. Open the Start menu and launch `PowerShell`.
2. Open `VS Code` if it is already installed. If not, use the links in the Installations section above to install `VS Code`, `Node.js`, and `Git`.
3. In PowerShell, type `cd` followed by the folder path for this project so you are inside `C:\Users\Admin\CloudGuard AI`.
4. Right-click inside the folder in File Explorer and choose `Open in Terminal` if that is easier for you.
5. Create the React app in a new `frontend` folder.

Before you run the command below, know that it creates the starter React project and downloads the files we need.

```powershell
npm create vite@latest frontend -- --template react
```

Expected result: Vite asks a few questions and then creates a `frontend` folder with React files inside it.

6. Open the new `frontend` folder in VS Code.
7. Open the terminal inside VS Code by clicking `Terminal` > `New Terminal`.
8. Install the project dependencies.

Before you run this command, know that it downloads the packages the React app needs to start.

```powershell
npm install
```

Expected result: npm finishes without errors and creates the `node_modules` folder.

9. Start the development server.

Before you run this command, know that it launches the local React website so you can see your changes in the browser.

```powershell
npm run dev
```

Expected result: the terminal shows a local address such as `http://localhost:5173`.

Verification:

- Open the local URL in your browser.
- Check that the React starter page appears.
- Make sure the terminal stays running and does not show an error.

Common mistakes and fixes:

- If `npm` is not recognized, reinstall Node.js and open a new terminal.
- If the port is already in use, close the old dev server and run the command again.
- If the page does not open, copy the local URL from the terminal and paste it into the browser.

Checklist:

- [ ] VS Code, Node.js, and Git are installed
- [ ] `frontend` project folder exists
- [ ] Dependencies are installed
- [ ] React app runs with `npm run dev`

Day 2: Create the first reusable components and understand the folder structure

Today's goal: build the first small UI pieces so the dashboard is not just one big page.

Simple language:

- A `component` is a small reusable piece of the screen.
- A `folder structure` keeps files organized so the project does not become messy.
- A `page` is a full screen.

Step-by-step:

1. Open the `frontend` folder in VS Code if it is not already open.
2. In the left sidebar, click `src`.
3. Right-click `src` and create a new folder named `components`.
4. Inside `components`, create two files: `Layout.jsx` and `Header.jsx`.
5. Open `Layout.jsx` and type a simple wrapper component that shows a main page container.
6. Open `Header.jsx` and type a simple title bar for the dashboard.
7. Open `src/App.jsx` and replace the starter content with the `Header` and `Layout` components.
8. Save all files with `Ctrl+S`.

What you are typing is simple React code that turns small building blocks into one dashboard screen.

Expected result: the browser updates and shows your custom header and page layout instead of the default Vite screen.

Verification:

- Confirm the browser refreshes automatically after you save.
- Check that both components appear in the app.
- Make sure there are no red error messages in the browser or terminal.

Common mistakes and fixes:

- If the screen stays blank, check that the file names end in `.jsx`.
- If a component does not appear, confirm you imported it in `App.jsx`.
- If the browser shows an error, read the first line carefully because it usually points to the missing file or typo.

Checklist:

- [ ] `components` folder exists
- [ ] `Layout.jsx` exists
- [ ] `Header.jsx` exists
- [ ] `App.jsx` uses the new components

Day 3: Pass simple data into a score card with props and state

Today's goal: show one dashboard value using data that can change later.

Simple language:

- `Props` are inputs you send to a component.
- `State` is data a component remembers and can change.
- A `score card` is a small box that shows one important number.

Step-by-step:

1. Open `src/components`.
2. Create a new file named `SecurityScoreCard.jsx`.
3. Type a component that receives a `score` prop and displays it on the screen.
4. Open `src/App.jsx`.
5. Create a small piece of state that holds a sample score value such as `82`.
6. Pass that score into `SecurityScoreCard`.
7. Change the value once and save the file so you can see the number update.

Before you test anything, know that this step teaches the dashboard how to show changing scan data later.

Expected result: the browser shows a score card with the number you set in state.

Verification:

- Change the score from `82` to `64` and save the file.
- Confirm the browser updates the number without a full page reload.
- Check that the component still renders when the number changes.

Common mistakes and fixes:

- If the score does not appear, check that the prop name matches in both files.
- If React shows an error about state, make sure `useState` is imported from React.
- If the card looks broken, confirm the component returns only one parent element.

Checklist:

- [ ] `SecurityScoreCard.jsx` exists
- [ ] Score is passed through props
- [ ] State changes update the screen
- [ ] The score card renders correctly

Day 4: Add Tailwind CSS so the dashboard looks clean and organized

Today's goal: turn plain elements into a dashboard that feels polished and easy to scan.

Simple language:

- `Tailwind CSS` is a styling tool made of small class names.
- A `layout` controls spacing and alignment.
- `Badges` are small colored labels that show status such as severity.

Step-by-step:

1. Open the VS Code terminal.
2. Install the Tailwind packages if they are not already part of the project.

Before you run the command below, know that it adds the styling tools React will use.

```powershell
npm install -D tailwindcss postcss autoprefixer
```

Expected result: npm adds the styling packages to the project.

3. Create the Tailwind config file.

Before you run the command below, know that it prepares Tailwind to read your project files.

```powershell
npx tailwindcss init -p
```

Expected result: Tailwind creates configuration files in the `frontend` folder.

4. Open the main CSS file in `src` and add the Tailwind directives.
5. Open `App.jsx` and replace plain spacing with Tailwind classes for padding, grids, and card spacing.
6. Add a few severity badge colors in your component code so different risk levels look different.

Expected result: the dashboard has spacing, card styling, and color differences that are easier to read.

Verification:

- Refresh the browser and confirm the page no longer looks plain.
- Check that the cards align neatly.
- Make sure the colored labels are readable.

Common mistakes and fixes:

- If Tailwind classes do nothing, check the CSS file import in `main.jsx`.
- If the config command fails, confirm you are inside the `frontend` folder.
- If colors do not show, verify the class names are spelled exactly right.

Checklist:

- [ ] Tailwind packages are installed
- [ ] Tailwind config files exist
- [ ] Main CSS includes Tailwind directives
- [ ] Dashboard spacing and badges look cleaner

Day 5: Call the backend health endpoint and show whether the backend is online

Today's goal: connect the frontend to the backend for the first time.

Simple language:

- An `API` is a door the frontend uses to ask the backend for data.
- `fetch` or `axios` sends a request to that door.
- A `health endpoint` is a simple check that says whether the server is alive.

Step-by-step:

1. Open `src/api` and create a new file named `client.js` if it does not already exist.
2. Type the backend base URL in that file so the app knows where to send requests.
3. Create a small helper function that calls `/api/health`.
4. Open `App.jsx` or the main dashboard page and call that helper when the page loads.
5. Show one message when the backend is online and a different message when it is offline.

Before you run the code, know that this step proves the frontend can talk to Student 2's backend.

If you need the package first, install it now.

```powershell
npm install axios
```

Expected result: the app can make a request and show a live backend status message.

Verification:

- Start the backend before opening the frontend.
- Refresh the page and confirm the "online" message appears.
- Stop the backend and confirm the offline message appears.

Common mistakes and fixes:

- If the request fails, check that the backend URL is correct.
- If the browser shows a CORS error, ask Student 2 to add `http://localhost:5173` to the FastAPI CORS allowed origins list. In production this will change to your Vercel URL.
- If the message never changes, confirm the request runs inside `useEffect`.

Checklist:

- [ ] `client.js` exists
- [ ] Frontend can call `/api/health`
- [ ] Online and offline messages work
- [ ] First frontend-backend connection is working

### Week 2

Day 6:

- Learn: Tables.
- Why: Findings are easiest to show in a table.
- Build: FindingsTable with dummy data.
- Outcome: Findings display clearly.

Day 7:

- Learn: Filtering.
- Why: Users need to filter by severity and service.
- Build: Severity and service dropdowns.
- Outcome: Table filters work.

Day 8:

- Learn: Charts using Recharts.
- Why: Charts make the dashboard demo-friendly.
- Build: Severity pie chart.
- Outcome: Risk summary is visual.

Day 9:

- Learn: Loading and error states.
- Why: APIs may take time or fail.
- Build: Loading spinner and error message.
- Outcome: UI does not look broken during waits.

Day 10:

- Learn: Environment variables in frontend.
- Why: API URL changes between local and deployed app.
- Build: `VITE_API_BASE_URL`.
- Outcome: API base URL is configurable.

### Week 3

Day 11:

- Connect to Student 2's scan API.
- Build: Run Scan button.
- Outcome: Button triggers backend scan.

Day 12:

- Connect findings API.
- Build: Show real findings after scan.
- Outcome: Dashboard displays backend data.

Day 13:

- Improve UI spacing and colors.
- Build: Severity badges.
- Outcome: Findings are easy to read.

Day 14:

- Test with different fake responses.
- Build: Empty state.
- Outcome: UI handles no findings.

Day 15:

- Integration checkpoint with Student 2.
- Outcome: Scan flow works from UI to backend.

### Week 4

Day 16:

- Learn: AI explanation panel.
- Build: Side panel layout.
- Outcome: User has place to view explanation.

Day 17:

- Connect Explain & Fix API.
- Build: Button per finding.
- Outcome: AI explanation appears.

Day 18:

- Add loading state for AI button.
- Outcome: Duplicate clicks are prevented.

Day 19:

- Display remediation steps as a checklist.
- Outcome: AI output is readable.

Day 20:

- Integration checkpoint with Student 3.
- Outcome: AI flow works end to end.

### Week 5

Day 21:

- Add report download button.
- Outcome: User can request PDF.

Day 22:

- Test PDF download in browser.
- Outcome: File downloads successfully.

Day 23:

- Make dashboard responsive.
- Outcome: UI works on laptop and mobile width.

Day 24:

- Add toast notifications.
- Outcome: Success and failure messages are clear.

Day 25:

- Full UI cleanup.
- Outcome: Demo-ready dashboard.

### Week 6

Day 26:

- Prepare Vercel deployment.
- Outcome: Frontend pushed to GitHub.

Day 27:

- Deploy frontend to Vercel.
- Outcome: Public frontend URL works.

Day 28:

- Connect deployed frontend to Railway backend.
- Outcome: Production API connection works.

Day 29:

- Practice demo flow.
- Outcome: You can explain every screen.

Day 30:

- Final bug fixing and backup screenshots.
- Outcome: Frontend is ready for review.

## 11. Testing Instructions

Test 1: Frontend starts.

```powershell
npm run dev
```

Expected: Browser opens or terminal shows local URL.

Common error: `missing script dev`.

Fix: Make sure you are inside the `frontend` folder.

Test 2: Backend health appears.

Expected: UI shows backend online.

Common error: CORS error in browser console.

Fix: Ask Student 2 to allow the frontend URL in backend CORS settings. During local development, the allowed origin is `http://localhost:5173`. In production, it will be your Vercel deployment URL such as `https://cloudguard-ai.vercel.app`. Student 2 must add both origins to the FastAPI CORS middleware.

Test 3: Run scan button works.

Expected: Score and findings update.

Common error: API URL wrong.

Fix: Check `VITE_API_BASE_URL`.

## 12. Viva Answers For Student 1

Question: What did you build?

Answer: I built the React dashboard that lets users run scans, view risk score, filter findings, request AI explanations, and download reports.

Question: How does frontend communicate with backend?

Answer: It sends HTTP requests to FastAPI endpoints and receives JSON responses.

Question: Why React?

Answer: React makes it easy to build reusable dashboard components.

Question: Why Tailwind?

Answer: Tailwind helps us design a clean UI quickly without writing large CSS files.
