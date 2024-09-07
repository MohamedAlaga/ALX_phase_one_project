import Image from "next/image";
import { leagueSpartan, lexend, manrope } from "../layout";

export default function Home() {
  return (
    <main>
      <div className="h-screen flex flex-col">
        <header className='flex bg-white tracking-wide sticky min-h-14 max-h-14 items-center px-4	border-solid border-b-2'>
          <Image className="min-h-10 max-h-10" src="/logo2.png" alt="logo" width={36} height={36} />
          <div className="text-3xl px-1">
            <h1 className={lexend.className}>ROLAX</h1>
          </div>
        </header>

        <div className="relative w-full h-48">
          <div className="relative top-0 left-0 w-full h-full bg-customPurple">
            <div className="flex justify-between items-center h-full px-24 text-5xl text-white font-bold">
              <p className={leagueSpartan.className}>Mohamed Alaga</p>
              <p className={leagueSpartan.className}>Manager</p>
            </div>
            <Image
              className="w-full h-full object-cover mix-blend-soft-light"
              src="/drugs.png"
              alt="drugs"
              layout="fill"
              objectFit="cover"
            />
          </div>
        </div>
        <div className="flex-1 flex px-11 py-11 overflow-auto ">
          <div className="w-6/12 px-11 flex justify-between h-full flex-col text-xl font-normal" style={ manrope.style}>
            <div>
              User name
              <input className="h-16 border border-customPurple rounded-md w-full" type="text" placeholder="  Enter user Name" />
            </div>
            <div>
              User name
              <input className="h-16 border border-customPurple rounded-md w-full" type="text" placeholder="  Enter user Name" />
            </div>
            <div>
              User name
              <input className="h-16 border border-customPurple rounded-md w-full" type="text" placeholder="  Enter user Name" />
            </div>
            <div>
              User name
              <input className="h-16 border border-customPurple rounded-md w-full" type="text" placeholder="  Enter user Name" />
            </div>
            <div>
              User name
              <input className="h-16 border border-customPurple rounded-md w-full" type="text" placeholder="  Enter user Name" />
            </div>
          </div>
          <div className="w-6/12 px-11 flex justify-between h-full flex-col text-3xl">
          <div className="h-16  rounded-md w-full flex justify-between items-center">
            <h1>Sell screen</h1>
            <input type="checkbox" className="custom-checkbox"/>
          </div>
          <div className="h-16  rounded-md w-full flex justify-between items-center">
            <h1>Buy screen</h1>
            <input type="checkbox" className="custom-checkbox"/>
          </div>
          <div className="h-16  rounded-md w-full flex justify-between items-center">
            <h1>Items screen</h1>
            <input type="checkbox" className="custom-checkbox"/>
          </div>
          <div className="h-16  rounded-md w-full flex justify-between items-center">
            <h1>Users screen</h1>
            <input type="checkbox" className="custom-checkbox" />
          </div>
          <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex  items-center justify-center text-white text-2xl">Save</button>
          </div>
        </div>
      </div>
    </main>
  );
}
// border border-customPurple 