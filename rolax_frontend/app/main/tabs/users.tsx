"use client";
import { manrope } from "@/app/layout";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useRef, useEffect, useState } from "react";

export default function usersTab() {
  var searchname = useRef<HTMLInputElement>(null);
  var [isLoading, setIsLoading] = useState(true);
  var AllusersList: Array<any> = [];
  var [usersList, setUsersList] = useState<Array<any>>([]);
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

  const getAllUsers = async () => {
    try {
      let response = await fetch("http://localhost:8000/api/users/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      let users = await response.json();
      if (response.status !== 200) {
        return [];
      }
      return users;
    } catch (error) {
      console.error("Error fetching users:", error);
      return [];
    }
  };
  useEffect(() => {
    const fetchRecieptsNumber = async () => {
      setIsLoading(false);
      AllusersList = await getAllUsers();
      setUsersList(AllusersList);
    };
    fetchRecieptsNumber();
  }, []);

  const getUsersSearch = async () => {
    refrechToken();
    AllusersList = await getAllUsers();
    const filteredUsers = AllusersList.filter((user: any) =>
      user["name"].toLowerCase().includes(searchname.current!.value.toLowerCase())
    );
    const newList = filteredUsers;
    console.log(AllusersList);
    console.log(newList);
    setUsersList(newList);
  };

  return (
    <main className="py-6 px-12">
      <div className="grid grid-rows-1 grid-cols-6 text-3xl items-center place-items-center gap-6 py-6">
        <Link href={"../addUser"} className="h-16 bg-violet-600 rounded-md w-full py-3 flex  items-center justify-center text-white text-2xl col-span-2">Add user</Link>
        <p>Name</p>
        <input
          className="w-full h-16 border-solid border-violet-600 border-2 rounded-md col-span-2"
          type="text"
          ref={searchname}
          onChange={(e) => searchname.current!.value = e.target.value}
        />
        <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex  items-center justify-center text-white text-2xl" onClick={getUsersSearch}>Search</button>
      </div>
      <div className={manrope.className}>
        <div className="my-6 border  border-slate-300 rounded-lg">
          <table className="w-full text-3xl text-center bg-white rounded-lg">
            <thead className="grid grid-cols-[0.5fr_2fr_2fr] w-full">
              <tr className="contents">
                <th scope="col" className=" py-3 border-r border-slate-300">
                  ID
                </th>
                <th scope="col" className=" py-3 border-r border-slate-300">
                  Name
                </th>
                <th scope="col" className=" py-3 border-r border-slate-300">
                  Email
                </th>
              </tr>
            </thead>
            <tbody className="grid grid-cols-[0.5fr_2fr_2fr] w-full">
              {usersList.map((user, index) => (
                <tr className=" border-t border-slate-300 contents" key={"row" + index}>
                  <td scope="row" className="py-4 border-r border-t border-slate-300" key={"row" + index + "col1"}>
                    {index}
                  </td>
                  <td className="py-4 border-r border-t border-slate-300" key={"row" + index + "col2"}>
                    {user["name"]}
                  </td>
                  <td className="py-4 border-r border-t border-slate-300" key={"row" + index + "col3"}>
                    {user["email"]}
                  </td>
                </tr>))}
            </tbody>
          </table>
        </div>
      </div>


    </main>
  );
}
