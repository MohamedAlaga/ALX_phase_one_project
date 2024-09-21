"use client";
import Image from "next/image";
import { lexend } from "../layout";
import { manrope } from "../layout";
import sellIconWhite, { buyIconBlack, buyIconwhite, itemsIconBlack, itemsIconWhite, sellIconblack, usersIconBlack, usersIconWhite } from "./components";
import { useState } from "react";
import SellTab from "./tabs/sell";
import BuyTab from "./tabs/buy";
import ItemsTab from "./tabs/items";
import UsersTab from "./tabs/users";
import { useRouter } from "next/navigation";


export default function Home() {
  const router = useRouter();
  const refrechToken = async () => {
    try {
      let response = await fetch("http://localhost:8000/api/users/refresh-token", {
        method: "Post",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      if (response.status !== 200) {
        alert("your session has expiered please login again");
        router.push("./login");
        return "0";
      }
      return "1";
    } catch (error) {
      alert("your session has expiered please login again");
      router.push("./login");
      return "0";
    }
  };
  var selectedButton = "bg-violet-600 rounded-md w-full py-3 flex text-lg items-center justify-center text-white";
  var unselectedButton = "rounded-md w-full py-3 flex text-lg items-center justify-center";
  var [selectedTab, setSelectedTab] = useState(0);
  const selectedtabhandler = (tab: number) => {
    refrechToken();
    setSelectedTab(selectedTab = tab);
  };
  return (
    <main className="h-screen">
      <header className='flex bg-white tracking-wide sticky min-h-14 max-h-14 items-center px-4	border-solid border-b-2'>
        <Image className="min-h-10 max-h-10" src="/logo2.png" alt="logo" width={36} height={36} />
        <div className="text-3xl px-1"><h1 className={lexend.className}>ROLAX</h1></div>
      </header>
      <div className="flex h-full">
        <div className="flex items-center flex-col center min-w-48 h-full border-solid border-r-2 py-6 px-6">
          <button onClick={(event) => selectedtabhandler(0)} className={selectedTab == 0 ? selectedButton : unselectedButton}>{selectedTab == 0 ? sellIconWhite() : sellIconblack()}<div className={manrope.className}>Sell</div></button>
          <button onClick={(event) => selectedtabhandler(1)} className={selectedTab == 1 ? selectedButton : unselectedButton}>{selectedTab == 1 ? buyIconwhite() : buyIconBlack()}<div className={manrope.className}>Buy</div></button>
          <button onClick={(event) => selectedtabhandler(2)} className={selectedTab == 2 ? selectedButton : unselectedButton}>{selectedTab == 2 ? itemsIconWhite() : itemsIconBlack()}items</button>
          <button onClick={(event) => selectedtabhandler(3)} className={selectedTab == 3 ? selectedButton : unselectedButton}>{selectedTab == 3 ? usersIconWhite() : usersIconBlack()}users</button>
        </div>
        <div className="w-full ">
          {selectedTab == 0 ? <SellTab /> : selectedTab == 1 ? <BuyTab /> : selectedTab == 2 ? <ItemsTab /> : <UsersTab />}
        </div>
      </div>
    </main>
  );
}