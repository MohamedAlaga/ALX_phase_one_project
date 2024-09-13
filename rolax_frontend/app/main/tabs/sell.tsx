"use client";
import { manrope } from "@/app/layout";
import { useRef, useEffect, useState } from "react";

export default function SellTab() {
  const recieptsNumberRef = useRef<string | null>(null);
  const dateRef = useRef<string>();
  var [barcode, setBarcode] = useState<string>(""); // Use state instead of ref for barcode
  var [items, setItems] = useState<Array<{ item_name: string }> | null>(null);
  var [isLoading, setIsLoading] = useState(true);
  var [showDropdown, setShowDropdown] = useState(false);
  var [searchTerm, setSearchTerm] = useState("");
  var [count, setCount] = useState(0);
  var [itemsList, setItemsList] = useState<Array<any>>([]);

  const getRecieptsNumber = async () => {
    try {
      let response = await fetch("http://localhost:8000/api/sell/last", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      let Reciepts = await response.json();
      if (response.status === 404) {
        return "1";
      } else if (response.status !== 200) {
        return "0";
      }
      return Reciepts[0]["recieptNumber"] + 1;
    } catch (error) {
      console.error("Error fetching receipt number:", error);
      return "0";
    }
  };

  async function searchItem(name: string) {
    try {
      let response = await fetch(
        "http://localhost:8000/api/items/search/" + name,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        }
      );
      let items = await response.json();
      if (response.status !== 200) {
        return null;
      }
      return items;
    } catch (error) {
      return null;
    }
  }

  useEffect(() => {
    const fetchRecieptsNumber = async () => {
      const number = await getRecieptsNumber();
      recieptsNumberRef.current = number;
      setIsLoading(false);
    };
    fetchRecieptsNumber();
    dateRef.current = new Date().toISOString().split("T")[0];
  }, []);

  const handleNameChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const term = event.target.value.trim();
    setSearchTerm(term);
    if (term.length > 0) {
      const items = await searchItem(term);
      if (items) {
        setItems(items);
        setShowDropdown(true);
      }
    } else {
      setItems(null);
      setShowDropdown(false);
    }
  };

  const handleItemSelect = (item: any) => {
    setBarcode(item["barcode"]);
    setSearchTerm(item["item_name"]);
    setShowDropdown(false);
  };

  const getItemByBarcode = async (barcode: string) => {
    try {
      let response = await fetch(
        "http://localhost:8000/api/items/barcode/" + barcode,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        }
      );
      let item = await response.json();
      if (response.status !== 200) {
        return {};
      }
      item["quantity"] = count;
      return item;
    } catch (error) {
      return {};
    }
  };

  const handleAdd = async () => {
    const newItem = await getItemByBarcode(barcode);
    if (newItem["item_name"]) { setItemsList([...itemsList, newItem]) }
  };

  const sellItems = async () => {
    const response = await fetch("http://localhost:8000/api/sell/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(itemsList.map((item) => ({ id: item["item_id"], quantitiy: item["quantity"] })),),
      credentials: "include",
    });
    recieptsNumberRef.current = await getRecieptsNumber();
    dateRef.current = new Date().toISOString().split("T")[0];
    searchTerm = "";
    barcode = "";
    count = 0;
    setItemsList([]);

  };

  async function getReciepts(number: number) {
    try {
      const lastRecieptNumber = await getRecieptsNumber() + 1;
      if (number === 0 || number > lastRecieptNumber) { return null };
      let response = await fetch("http://localhost:8000/api/sell/" + number, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      let Reciepts = await response.json();
      if (response.status === 404) {
        searchTerm = "";
        barcode = "";
        count = 0;
        recieptsNumberRef.current = String(number);
        setItemsList([]);
        return null;
      }
      else if
        (response.status !== 200) {
        return null;
      };
      searchTerm = "";
      barcode = "";
      count = 0;
      recieptsNumberRef.current = Reciepts[0]["recieptNumber"];
      setItemsList(Reciepts);
      return Reciepts;
    } catch (error) {
      return null;
    }
  };

  const handlePrevious = async () => {
    const recNumber = Number(recieptsNumberRef.current) - 1;
    getReciepts(recNumber);
  }
  const handleNext = async () => {
    const recNumber = Number(recieptsNumberRef.current) + 1;
    getReciepts(recNumber);
  }

  return (
    <main className="py-6 px-12">
      <div className="grid grid-rows-2 grid-cols-6 text-3xl items-center place-items-center gap-6 py-6" >
        <p className={manrope.className}>Reciepts</p>
        <input
          className="w-full h-16 border-solid border-violet-600 border-2 rounded-md text-center"
          type="text"
          value={isLoading ? "Loading..." : recieptsNumberRef.current || ""}
          disabled
        />
        <p>Barcode</p>
        <input
          className="w-full h-16 border-solid border-violet-600 border-2 rounded-md px-2"
          type="text"
          value={barcode}
          onChange={(e) => setBarcode(e.target.value)}
        />
        <p>Count</p>
        <input
          className="w-full h-16 border-solid border-violet-600 border-2 rounded-md text-center"
          type="text"
          value={Number.isNaN(count) ? "" : count}
          onChange={(e) => setCount(parseInt(e.target.value))}
        />
        <p>Date</p>
        <input
          className="w-full h-16 border-solid border-violet-600 border-2 rounded-md text-2xl text-center"
          type="text"
          value={dateRef.current || ""}
          disabled
        />
        <p>Name</p>

        <div className="relative w-full h-16 col-span-2">
          <input
            className="w-full h-full px-2 border-solid border-violet-600 border-2 rounded-md"
            onChange={handleNameChange}
            value={searchTerm}
          />

          {showDropdown && items && (
            <ul className="absolute z-10 w-full bg-white border border-gray-300 rounded-md mt-1 max-h-48 overflow-y-auto shadow-lg">
              {items.map((item, index) => (
                <li
                  key={index}
                  className="px-4 py-2 hover:bg-gray-200 cursor-pointer"
                  onClick={() => handleItemSelect(item)}
                >
                  {item.item_name}
                </li>
              ))}
            </ul>
          )}
        </div>

        <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex items-center justify-center text-white text-2xl" type="submit" onClick={handleAdd}>
          Add
        </button>
      </div>
      <div className={manrope.className}>
        <div className="my-6 border border-slate-300 rounded-lg">
          <table className="w-full text-3xl text-center bg-white rounded-lg">
            <thead className="grid grid-cols-[0.5fr_3fr_1fr_1fr_1fr] w-full">
              <tr className="contents">
                <th scope="col" className="py-3 border-r border-slate-300">
                  ID
                </th>
                <th scope="col" className="py-3 border-r border-slate-300">
                  Name
                </th>
                <th scope="col" className="py-3 border-r border-slate-300">
                  Count
                </th>
                <th scope="col" className="py-3 border-r border-slate-300">
                  Price
                </th>
                <th scope="col" className="py-3">
                  total
                </th>
              </tr>
            </thead>
            <tbody className="grid grid-cols-[0.5fr_3fr_1fr_1fr_1fr] w-full">
              {itemsList.map((item, index) => (
                <tr className="border-t border-slate-300 contents" key={"row" + index}>
                  <td
                    scope="row"
                    className="py-4 border-r border-t border-slate-300"
                    key={"row" + index + "col1"}
                  >
                    {index + 1}
                  </td>
                  <td className="py-4 border-r border-t border-slate-300"
                    key={"row" + index + "col2"}
                  >
                    {item["item_name"]}
                  </td>
                  <td className="py-4 border-r border-t border-slate-300"
                    key={"row" + index + "col3"}>
                    {item["quantity"]}
                  </td>
                  <td className="py-4 border-r border-t border-slate-300"
                  key={"row" + index + "col4"}>
                    {item["price"]}
                  </td>
                  <td className="py-4 border-t border-slate-300">{item["price"] * item["quantity"]}</td>
                </tr>))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="grid grid-rows-2 grid-cols-6 text-3xl items-center place-items-center gap-6 py-6">
        <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex text-2xl items-center justify-center text-white" onClick={handlePrevious}>
          Previous
        </button>
        <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex text-2xl items-center justify-center text-white" onClick={handleNext}>
          Next
        </button>
        <div></div>
        <div></div>
        <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex text-2xl items-center justify-center text-white col-span-2" onClick={sellItems}>
          Save
        </button>
      </div>
    </main>
  );
}
