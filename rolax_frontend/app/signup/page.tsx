"use client";
import Image from "next/image";
import { leagueSpartan, manrope } from "../layout";
import { useState, useRef } from "react";
import { useRouter } from "next/navigation"
import Link from "next/link";
export default function Home() {
  const router = useRouter();
  const emailRef = useRef<HTMLInputElement>(null);
  const nameRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const confirmPasswordRef = useRef<HTMLInputElement>(null);
  const [showDialog, setShowDialog] = useState(false);
  const [dialogMessage, setDialogMessage] = useState("");

  const handleSignup = async (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    const name = nameRef.current?.value || "";
    const email = emailRef.current?.value || "";
    const password = passwordRef.current?.value || "";
    const confirmPassword = confirmPasswordRef.current?.value || "";
    if (password !== confirmPassword) {
      setDialogMessage("Passwords do not match.");
      setShowDialog(true);
      return;
    }
    const response = await fetch("http://localhost:8000/api/users/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        email,
        password,
      }),
    });
    var body = await response.json();

    if (body["email"] != null) {
      setDialogMessage("Email already exists.");
      setShowDialog(true);
    }
    else if (response.status !== 200) {
      setDialogMessage("An error occurred. Please try again.");
      setShowDialog(true);
    } else {
      setShowDialog(false);
      router.push("../login");
    }
  };
  return (
    <main className="h-screen bg-gray-50 flex items-center justify-center">
      <form className="flex flex-col w-[36.25rem] bg-white h-[54rem] rounded-md drop-shadow-lg p-9 justify-center items-center" onSubmit={handleSignup}>
        <Image className="h-[4.375rem] w-[5.125rem] mb-10" src="/logo2.png" alt="logo" width={82} height={70} />
        <p className="text-[4rem] font-black" style={leagueSpartan.style}>
          JOIN ROLAX
        </p>
        <p className="mt-[1.12rem] text-4xl" style={leagueSpartan.style}>
          Sign up for free!
        </p>
        <input className="text-[1.125rem] border border-customPurple h-[4.25rem] rounded-md mt-[1.12rem] w-full px-4" type="text" placeholder="Enter user Name" ref={nameRef} />
        <input className="text-[1.125rem] border border-customPurple h-[4.25rem] rounded-md mt-[1.12rem] w-full px-4" type="text" placeholder="Enter user Email" ref={emailRef} />
        <input className="text-[1.125rem] border border-customPurple h-[4.25rem] rounded-md mt-[1.12rem] w-full px-4" type="password" placeholder="Enter user password" ref={passwordRef} />
        <input className="text-[1.125rem] border border-customPurple h-[4.25rem] rounded-md mt-[1.12rem] w-full px-4" type="password" placeholder="Confirm your password" ref={confirmPasswordRef} />
        <button className="bg-customPurple w-full text-white mt-[1.12rem] h-[4.25rem] rounded-md  text-2xl font-extrabold" style={manrope.style} type="submit"> Create Account</button>
        {/* Display error message */}
        {showDialog && (
          <div className="w-full bg-red-100 text-red-600 border border-red-600 rounded-md mt-[1.12rem] p-4 ">
            <p>{dialogMessage}</p>
          </div>
        )}
        <div className="mt-9">
          <p className="text-xl" style={manrope.style}>By clicking Create account, you agree to Rolax's privacy notice, T&Cs and to receive offers, news and updates.</p>
          <p className="text-xl mt-[1.12rem] " style={manrope.style}>Already have an account ? <Link href="../login" className="text-customPurple">Login</Link> </p>
        </div>
      </form>
    </main>
  );
}