import Header from "@/components/header";
import Transactions from "@/components/transactions";


export default function Home() {
  return (
    <main className="min-h-screen flex flex-col space-y-6 w-full">
      <Header/>
      <Transactions />
    </main>
  )
}