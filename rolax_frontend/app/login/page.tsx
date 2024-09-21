"use client";
import Image from "next/image";
import { leagueSpartan, manrope } from "../layout";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation"

export default function Home() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showDialog, setShowDialog] = useState(false);
  const [dialogMessage, setDialogMessage] = useState("");

  const router = useRouter();

  useEffect(() => {
    fetch("http://localhost:8000/api/users/current", {
      method: "GET", headers: {
        "Content-Type": "application/json",
      },credentials: "include",
    }).then((res) => res.status === 200 && router.push("../main"))
  }, [])

  const handleLogin = async (e: { preventDefault: () => void; }) => {
    e.preventDefault();

    const response = await fetch("http://localhost:8000/api/users/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }), credentials: "include",
    });

    if (response.status === 403) {
      setDialogMessage("Invalid login attempt.");
      setShowDialog(true);
    } else if (response.status !== 200) {
      setDialogMessage("An error occurred. Please try again.");
      setShowDialog(true);
    } else {
      setShowDialog(false);
      router.push("../main");
    }
  };

  return (
    <main className="h-screen bg-gray-50 flex items-center justify-center">
      <form
        className="flex flex-col w-[36.25rem] bg-white h-[49.3125rem] rounded-md drop-shadow-lg p-[2.2rem] justify-center items-center"
        onSubmit={handleLogin}
      >
        <Image
          className="h-[4.375rem] w-[5.125rem] mb-10"
          src="/logo2.png"
          alt="logo"
          width={82}
          height={70}
        />
        <p className="text-[4rem] font-black " style={leagueSpartan.style}>
          WELCOME BACK!
        </p>
        <p className="text-4xl" style={leagueSpartan.style}>
          login into Rolax
        </p>
        <p className="my-5 text-xl" style={manrope.style}>
          Empowering Your Pharmacy, One Prescription at a Time.
        </p>
        <input
          className="text-[1.125rem] border border-customPurple h-[4.25rem] rounded-md mt-[1.12rem] w-full px-4"
          type="text"
          placeholder="Enter Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="text-[1.125rem] border border-customPurple h-[4.25rem] rounded-md mt-[1.12rem] w-full px-4"
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          className="bg-customPurple w-full text-white mt-[1.12rem] h-[4.25rem] rounded-md  text-2xl font-extrabold"
          style={manrope.style}
          type="submit"
        >
          Login
        </button>

        {/* Display error message */}
        {showDialog && (
          <div className="w-full bg-red-100 text-red-600 border border-red-600 rounded-md mt-[1.12rem] p-4 ">
            <p>{dialogMessage}</p>
          </div>
        )}

        <div className="w-full mt-9">
          <p className="text-xl " style={manrope.style}>
            Forgot your Password?{" "}
            <Link href="/forgetPassword" className="text-customPurple">
              Reset password
            </Link>
          </p>
          <p className="text-xl mt-[1.12rem]" style={manrope.style}>
            Do not have an account?{" "}
            <Link href="/signup" className="text-customPurple">
              Sign up
            </Link>
          </p>
        </div>
      </form>
    </main>
  );
}