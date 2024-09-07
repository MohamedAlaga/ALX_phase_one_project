"use client";
import Image from "next/image";
import { lexend } from "../layout";
import { manrope } from "../layout";
import sellIconWhite, { buyIconBlack, buyIconwhite, itemsIconBlack, itemsIconWhite, sellIconblack, usersIconBlack, usersIconWhite } from "./components";
import {useState } from "react";
import sellTab from "./tabs/sell";
import buyTab from "./tabs/buy";
import itemsTab from "./tabs/items";
import usersTab from "./tabs/users";


export default function Home() {
  var selectedButton = "bg-violet-600 rounded-md w-full py-3 flex text-lg items-center justify-center text-white";
  var unselectedButton = "rounded-md w-full py-3 flex text-lg items-center justify-center";
  var [selectedTab, setSelectedTab] = useState(1);
  const selectedtabhandler = (tab:number) => {
    setSelectedTab(selectedTab=tab);
  };
  return (
    <main className="h-screen">
      <header className='flex bg-white tracking-wide sticky min-h-14 max-h-14 items-center px-4	border-solid border-b-2'>
        <Image className="min-h-10 max-h-10" src="/logo2.png" alt="logo" width={36} height={36} />
        <div className="text-3xl px-1"><h1 className={lexend.className}>ROLAX</h1></div>
      </header>
      <div className="flex h-full">
        <div className="flex items-center flex-col center min-w-48 h-full border-solid border-r-2 py-6 px-6">
          <button onClick={(event) => selectedtabhandler(0)} className={selectedTab == 0 ? selectedButton :unselectedButton}>{selectedTab == 0? sellIconWhite():sellIconblack()}<div className={manrope.className}>Sell</div></button>
          <button onClick={(event) => selectedtabhandler(1)} className={selectedTab == 1 ? selectedButton :unselectedButton}>{selectedTab == 1? buyIconwhite():buyIconBlack()}<div className={manrope.className}>Buy</div></button>
          <button onClick={(event) => selectedtabhandler(2)} className={selectedTab == 2 ? selectedButton :unselectedButton}>{selectedTab == 2? itemsIconWhite():itemsIconBlack()}items</button>
          <button onClick={(event) => selectedtabhandler(3)} className={selectedTab == 3 ? selectedButton :unselectedButton}>{selectedTab == 3? usersIconWhite():usersIconBlack()}users</button>
        </div>
        <div className="w-full ">
          {selectedTab == 0? sellTab():selectedTab == 1? buyTab():selectedTab == 2? itemsTab():usersTab()}
        </div>
      </div>
    </main>
  );
}