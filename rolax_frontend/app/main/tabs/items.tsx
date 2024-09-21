"use client";
import { manrope } from "@/app/layout";
import { useRouter } from "next/navigation";
import { useRef, useEffect, useState } from "react";

export default function itemsTab() {
  var [isLoading, setIsLoading] = useState(true);
  var [itemsList, setItemsList] = useState<Array<any>>([]);
  const barcodeRef = useRef<HTMLInputElement>(null);
  const nameRef = useRef<HTMLInputElement>(null);
  const priceRef = useRef<HTMLInputElement>(null);

  const getAllItems = async () => {
    try {
      let response = await fetch("http://localhost:8000/api/items/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      let items = await response.json();
      if (response.status !== 200) {
        return [];
      }
      return items;
    } catch (error) {
      console.error("Error fetching items:", error);
      return [];
    }
  };

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

  const addItem = async () => {
    refrechToken();
    try {
      let response = await fetch("http://localhost:8000/api/items/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          barcode: barcodeRef.current!.value,
          name: nameRef.current!.value,
          price: priceRef.current!.value,
        }),
      });
      if (response.status !== 200) {
        alert("Error adding item");
        return;
      }
      barcodeRef.current!.value = "";
      nameRef.current!.value  = "";
      priceRef.current!.value = "";
      setItemsList(await getAllItems());
    } catch (error) {
      alert("Error adding item");
      return;
    };
  };

  useEffect(() => {
    const fetchItems = async () => {
      let items = await getAllItems();
      setItemsList(items);
      setIsLoading(false);
    };
    fetchItems();
  }, []);

  return (
    <main className="py-6 px-12">
      <div className="grid grid-rows-2 grid-cols-6 text-3xl items-center place-items-center gap-6 py-6">
        <p>Barcode</p>
        <input
          ref={barcodeRef}
          className="w-full h-16 border-solid border-violet-600 border-2 rounded-md col-span-2 px-2"
          type="text"
          onChange={(e) => barcodeRef.current!.value = e.target.value}
        />
        <p>Name</p>
        <input
          ref={nameRef}
          className="w-full h-16 border-solid border-violet-600 border-2 rounded-md col-span-2 px-2"
          type="text"
          onChange={(e) => nameRef.current!.value = e.target.value}
        />
        <p>Sell Price</p>
        <input
          ref={priceRef}
          className="w-full h-16 border-solid border-violet-600 border-2 rounded-md col-span-2 px-2"
          type="text"
          onChange={(e) => {
            var text = e.target.value;
            if (Number.isNaN(parseFloat(text))) {
              priceRef.current!.value = "";
            } else if (text.includes(".")) {
              var split = text.split(".");
              if (Number.isNaN(parseInt(split[1]))) {
                priceRef.current!.value = parseInt(split[0]) + ".";
              }
              else {
                priceRef.current!.value = parseInt(split[0]) + "." + parseInt(split[1]);
              }
            } else {
              priceRef.current!.value = parseInt(text).toString();
            }
          }}
          inputMode="decimal"
        />
        <div></div>
        <button
          className="h-16 bg-violet-600 rounded-md w-full py-3 flex items-center justify-center text-white text-2xl col-span-2"
          onClick={addItem}
        >
          Add
        </button>
      </div>

      <div className={manrope.className}>
        <div className="my-6 border border-slate-300 rounded-lg">
          <table className="w-full text-3xl text-center bg-white rounded-lg">
            <thead className="grid grid-cols-[0.5fr_3fr_1fr_1fr] w-full">
              <tr className="contents">
                <th scope="col" className=" py-3 border-r border-slate-300">
                  ID
                </th>
                <th scope="col" className=" py-3 border-r border-slate-300">
                  Name
                </th>
                <th scope="col" className=" py-3 border-r border-slate-300">
                  Count
                </th>
                <th scope="col" className=" py-3">
                  Price
                </th>
              </tr>
            </thead>
            <tbody className="grid grid-cols-[0.5fr_3fr_1fr_1fr] w-full">
              {itemsList.map((item, index) => (
                <tr className="border-t border-slate-300 contents" key={"row" + index}>
                  <td className="py-4 border-r border-t border-slate-300">{index + 1}</td>
                  <td className="py-4 border-r border-t border-slate-300">{item["item_name"]}</td>
                  <td className="py-4 border-r border-t border-slate-300">{item["quantity"]}</td>
                  <td className="py-4 border-r border-t border-slate-300">{item["price"]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}