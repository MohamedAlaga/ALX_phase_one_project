import Image from "next/image";
import { leagueSpartan, manrope } from "../layout";

export default function Home() {
  return (
    <main className="h-screen bg-gray-50 flex items-center justify-center">
      <div className="flex flex-col w-[36.25rem] bg-white h-[49.3125rem] rounded-md drop-shadow-lg p-[2.2rem] justify-center items-center" >
        <Image className="h-[4.375rem] w-[5.125rem] mb-10" src="/logo2.png" alt="logo" width={82} height={70} />
        <p className="text-[4rem] font-black " style={leagueSpartan.style}>
         WELCOME BACK!
        </p>
        <p className=" text-4xl" style={leagueSpartan.style}>
        login into Rolax
        </p>
        <p className="my-5 text-xl" style={manrope.style}>
        Empowering Your Pharmacy, One Prescription at a Time.
        </p>
        <input className="text-[1.125rem] border border-customPurple h-[4.25rem] rounded-md mt-[1.12rem] w-full" type="text" placeholder="  Enter Email" />
        <input className="text-[1.125rem] border border-customPurple h-[4.25rem] rounded-md mt-[1.12rem] w-full" type="text" placeholder="  Enter password" />
        <button className="bg-customPurple w-full text-white mt-[1.12rem] h-[4.25rem] rounded-md mb-9 text-2xl font-extrabold" style={manrope.style}> Login</button>
        <div className="w-full">
        <p className="text-xl" style={manrope.style}>Forgot your Password ? <a href="" className="text-customPurple">Reset password</a></p>
        <p className="text-xl mt-[1.12rem] " style={manrope.style}>Already have an account ? <a href="" className="text-customPurple">Login</a> </p>
        </div>
      </div>
    </main>
  );
}