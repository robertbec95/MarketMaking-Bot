# Market Making Bot + Dashboard Project

## Backend (Python)

Technologies and Libraries:
- Python
- SQLite (via sqlite3)
- requests library
- time and random modules
- dataclasses

Key Components:
1. MarketMaker class (main.py):
   - Simulates market making activities
   - Interacts with external API for order book data
   - Places and manages orders
   - Updates balances

2. Database class (database.py):
   - Handles database operations
   - Creates tables for transactions and balances
   - Provides methods for adding transactions and updating balances

Main Functionality:
- Simulates placing buy (BID) and sell (ASK) orders
- Checks for filled orders and updates balances
- Periodically prints balance and transaction information
- Stores transactions and balance updates in SQLite database

## Frontend (Next.js)

Technologies and Libraries:
- Next.js (React framework)
- TypeScript
- Tailwind CSS
- Prisma ORM
- SQLite (via Prisma)

Key Components:
1. API Route (src/app/api/transactions/route.ts):
   - Fetches recent transactions and latest balance

2. Transactions Component (src/components/transactions.tsx):
   - Displays transactions and balance
   - Updates data every 5 seconds

3. Header Component (src/components/header.tsx):
   - Displays dashboard title

4. Prisma Schema (prisma/schema.prisma):
   - Defines Transactions and Balances models

Main Functionality:
- Fetches and displays recent transactions
- Shows latest ETH and USD balances
- Real-time updates every 5 seconds

## Setup Instructions

Frontend:
1. Navigate to frontend directory
2. Install dependencies: npm install
3. Rename .env.example to .env
4. Setup database: npx prisma generate && npx prisma db push
5. Run dev server: npm run dev
6. Access dashboard at http://localhost:3000


Backend:
1. Clone repository
2. Create virtual environment
3. Install dependencies (requests) pip install -r requirements.txt
4. Run: python main.py
