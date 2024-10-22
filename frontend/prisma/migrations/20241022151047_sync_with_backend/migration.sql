/*
  Warnings:

  - You are about to drop the `Balance` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Transaction` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "Balance";
PRAGMA foreign_keys=on;

-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "Transaction";
PRAGMA foreign_keys=on;

-- CreateTable
CREATE TABLE "Transactions" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "type" TEXT NOT NULL,
    "price" REAL NOT NULL,
    "amount" REAL NOT NULL,
    "timestamp" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateTable
CREATE TABLE "Balances" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "eth_balance" REAL NOT NULL,
    "usd_balance" REAL NOT NULL,
    "timestamp" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
