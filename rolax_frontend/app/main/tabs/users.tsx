import { manrope } from "@/app/layout";

export default function usersTab() {
  return (
    <main className="py-6 px-12">
      <div className="grid grid-rows-1 grid-cols-6 text-3xl items-center place-items-center gap-6 py-6">
        <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex  items-center justify-center text-white text-2xl col-span-2">Add user</button>
        <p>Name</p>
        <input className="w-full h-16 border-solid border-violet-600 border-2 rounded-md col-span-2" type="text" />
        <button className="h-16 bg-violet-600 rounded-md w-full py-3 flex  items-center justify-center text-white text-2xl">Search</button>
      </div>
      <div className={manrope.className}>
        <div className="my-6 border  border-slate-300 rounded-lg">
          <table className="w-full text-3xl text-center bg-white rounded-lg">
            <thead className="grid grid-cols-[0.5fr_2fr_2fr_1fr] w-full">
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
                <th scope="col" className=" py-3">
                  Job Title
                </th>
              </tr>
            </thead>
            <tbody className="grid grid-cols-[0.5fr_2fr_2fr_1fr] w-full">
              <tr className=" border-t border-slate-300 contents">
                <td scope="row" className="py-4 border-r border-t border-slate-300">
                  1
                </td>
                <td className="py-4 border-r border-t border-slate-300">
                  Mohamed Alaga
                </td>
                <td className="py-4 border-r border-t border-slate-300">
                  mohamed@gmail.com
                </td>
                <td className="py-4 border-t">
                  Manger
                </td>
              </tr>
              <tr className=" border-t border-slate-300 contents">
                <td scope="row" className="py-4 border-r border-t border-slate-300">
                  2
                </td>
                <td className="py-4 border-r border-t border-slate-300">
                  john mokaya
                </td>
                <td className="py-4 border-r border-t border-slate-300">
                  john@gmail.com
                </td>
                <td className="py-4 border-t">
                  Sales
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>


    </main>
  );
}
