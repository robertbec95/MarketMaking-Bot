"use client";





export default function Header() {
 

  return (
    <header className=" top-2 z-30 w-full">
      <div className="mx-auto max-w-6xl px-2 sm:px-6">
        <div className="relative flex h-14 items-center justify-between gap-3 rounded-2xl bg-black px-3 shadow-lg shadow-black/[0.03] backdrop-blur-sm before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:border before:border-transparent before:[background:linear-gradient(theme(colors.gray.100),theme(colors.gray.200))_border-box] before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)]">
          <div className="flex flex-1 items-center ml-2 text-xl font-bold text-white">
           Market Making Dashboard
          </div>

       
        </div>
      </div>
    </header>
  );
}
