import { Camp } from "@/components/Camp";

import Getapp from "@/components/Getapp";
import Guide from "@/components/Guide";
import Hero from "@/components/Hero";


const Login = () => {
  return (
    <div className="flex flex-col space-y-4">
      <input type="text" placeholder="Email or username" className="border rounded-lg p-2" />
      <input type="password" placeholder="Password" className="border rounded-lg p-2" />
      <button className="bg-purple-500 text-white rounded-lg p-2">Log in</button>
    </div>
  );
};

export default function Home() {
  return (
    <>
      <Hero />
      <Camp
      />
      <Guide />
   
      <Getapp />
    </>
  )
}