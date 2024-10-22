import { PrismaClient } from '@prisma/client'
import { NextResponse } from 'next/server'

const prisma = new PrismaClient()

export async function GET() {
  const recentTransactions = await prisma.transactions.findMany({
    take: 10,
    orderBy: { timestamp: 'desc' },
  })

  const latestBalance = await prisma.balances.findFirst({
    orderBy: { timestamp: 'desc' },
  })
  console.log(recentTransactions)
  console.log(latestBalance)

  return NextResponse.json({ recentTransactions, latestBalance })
}
