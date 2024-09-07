import { manrope } from "@/app/layout";

export default function buyTab() {
  return (
    <main className="py-6 px-12">
      <div className="grid grid-rows-2 grid-cols-6 text-3xl items-center place-items-center gap-6 py-6">
        <p className={manrope.className}>Reciepts</p>
        <input className="w-full h-16 border-solid border-violet-600 border-2 rounded-md col-span-2" type="text" />
        <p>barcode</p>
        <input className="w-full h-16 border-solid border-violet-600 border-2 rounded-md col-span-2" type="text" />
        <p>Date</p>
        <input className="w-full h-16 border-solid border-violet-600 border-2 rounded-md col-span-2" type="text" />
        <p>Name</p>
        <input className="w-full h-16 border-solid border-violet-600 border-2 rounded-md col-span-2" type="text" />
        <p>buy price</p>
        <input className="w-full h-16 border-solid border-violet-600 border-2 rounded-md" type="text" />
        <p>Count</p>
        <input className="w-full h-16 border-solid border-violet-600 border-2 rounded-md" type="text" />
        <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex  items-center justify-center text-white text-2xl col-span-2">Add</button>
      </div>
      <div className={manrope.className}> 
        <div className="my-6 border  border-slate-300 rounded-lg">
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
              <tr className=" border-t border-slate-300 contents">
                <td scope="row" className="py-4 border-r border-t border-slate-300">
                  1
                </td>
                <td className="py-4 border-r border-t border-slate-300">
                  Silver
                </td>
                <td className="py-4 border-r border-t border-slate-300">
                  Laptop
                </td>
                <td className="py-4 border-t">
                  $2999
                </td>
              </tr>
              <tr className=" border-t border-slate-300 contents">
                <td scope="row" className="py-4 border-r border-t border-slate-300">
                  2
                </td>
                <td className="py-4 border-r border-t border-slate-300">
                  White
                </td>
                <td className="py-4 border-r border-t border-slate-300">
                  Laptop PC
                </td>
                <td className="py-4 border-t">
                  $1999
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div className="grid grid-rows-2 grid-cols-6 text-3xl items-center place-items-center gap-6 py-6">
      <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex text-2xl items-center justify-center text-white ">Previous</button>
      <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex text-2xl items-center justify-center text-white ">Next</button>
      <div></div>
      <div></div>
      <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex text-2xl items-center justify-center text-white col-span-2">Save</button>
      </div>

    </main>
  );
}
