"use client";
import Image from "next/image";
import { leagueSpartan, lexend, manrope } from "../layout";
import { useRef } from "react";
import { useRouter } from "next/navigation"

export default function Home() {
  const userNameRef = useRef<HTMLInputElement>(null);
  const emailRef = useRef<HTMLInputElement>(null);
  const passRef = useRef<HTMLInputElement>(null);
  const confirmPassRef = useRef<HTMLInputElement>(null);
  const sellScreenRef = useRef<HTMLInputElement>(null);
  const buyScreenRef = useRef<HTMLInputElement>(null);
  const itemsScreenRef = useRef<HTMLInputElement>(null);
  const usersScreenRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const addUser = async () => {
    if (passRef.current!.value !== confirmPassRef.current!.value) {
      console.error("Passwords do not match");
      return false;
    }
    try {
      let response = await fetch("http://localhost:8000/api/users/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          name: userNameRef.current!.value,
          email: emailRef.current!.value,
          password: passRef.current!.value,
        }),
      });
      if (response.status !== 200) {
        console.error("Error adding user:", response.status);
        return false;
      }
      userNameRef.current!.value = "";
      emailRef.current!.value = "";
      passRef.current!.value = "";
      confirmPassRef.current!.value = "";
      const body = await response.json();
      return body["id"];
    } catch (error) {
      console.error("Error adding user:", error);
      return false;
    };
  };

  const assignPermissions = async (userId: number , permission:string) => {
    try {
      let response = await fetch("http://localhost:8000/api/users/perms/grant", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          user_id: userId,
          permission: permission,
        }),
      });
      if (response.status !== 200) {
        console.error("Error assigning permissions:", response.status);
        return false;
      }
      return true;
    } catch (error) {
      console.error("Error assigning permissions:", error);
      return false;
    };
  };

  const handleAddUser = async () => {
    const userId = await addUser();
    if (userId) {
      if (sellScreenRef.current!.checked) {
        assignPermissions(userId, "manage_sell_receipts");
      }
      if (buyScreenRef.current!.checked) {
        assignPermissions(userId, "manage_purchase_receipts");
      }
      if (itemsScreenRef.current!.checked) {
        assignPermissions(userId, "manage_items");
      }
      if (usersScreenRef.current!.checked) {
        assignPermissions(userId, "manage_users");
      }
      router.push("../main")
    }
  };

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
          <div className="w-6/12 px-11 flex justify-between h-full flex-col text-xl font-normal" style={manrope.style}>
            <div>
              User name
              <input
                className="h-16 border border-customPurple rounded-md w-full px-2"
                type="text"
                placeholder="Enter user Name"
                ref={userNameRef}
                onChange={(e) => userNameRef.current!.value = e.target.value} />
            </div>
            <div>
              Email
              <input
                className="h-16 border border-customPurple rounded-md w-full px-2"
                type="text"
                placeholder="Enter Email"
                ref={emailRef}
                onChange={(e) => emailRef.current!.value = e.target.value} />
            </div>
            <div>
              Password
              <input
                className="h-16 border border-customPurple rounded-md w-full px-2"
                type="password"
                placeholder="Enter Password"
                ref={passRef}
                onChange={(e) => passRef.current!.value = e.target.value} />
            </div>
            <div>
              Confirm Password
              <input
                className="h-16 border border-customPurple rounded-md w-full px-2"
                type="password"
                placeholder="Enter Confirm Password"
                ref={confirmPassRef}
                onChange={(e) => confirmPassRef.current!.checked = e.target.checked} />
            </div>
            <div>
              <div className="h-16 bg-transparent rounded-md w-full py-3 flex  items-center justify-center text-white text-2xl"></div>
            </div>
          </div>
          <div className="w-6/12 px-11 flex justify-between h-full flex-col text-3xl">
            <div className="h-16  rounded-md w-full flex justify-between items-center">
              <h1>Sell screen</h1>
              <input type="checkbox" className="custom-checkbox" ref={sellScreenRef} onChange={(e) => sellScreenRef.current!.checked = e.target.checked}/>
            </div>
            <div className="h-16  rounded-md w-full flex justify-between items-center">
              <h1>Buy screen</h1>
              <input type="checkbox" className="custom-checkbox" ref={buyScreenRef} onChange={(e) => buyScreenRef.current!.checked = e.target.checked}/>
            </div>
            <div className="h-16  rounded-md w-full flex justify-between items-center">
              <h1>Items screen</h1>
              <input type="checkbox" className="custom-checkbox" ref={itemsScreenRef} onChange={(e) => itemsScreenRef.current!.checked = e.target.checked}/>
            </div>
            <div className="h-16  rounded-md w-full flex justify-between items-center">
              <h1>Users screen</h1>
              <input type="checkbox" className="custom-checkbox" ref={usersScreenRef} />
            </div>
            <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex  items-center justify-center text-white text-2xl" onClick={handleAddUser}>Save</button>
          </div>
        </div>
      </div>
    </main>
  );
}