import testProfileImg from "../../assets/tellYourStoryImg.svg"
import { IoMdNotificationsOutline } from "react-icons/io";
import { CiSearch } from "react-icons/ci";


const DashboardHeader = () => {
  return (
    <main className="grid grid-cols-[90%_6%] lg:grid-cols-[55%_35%_6%] gap-3 w-full items-center">

        <section className="flex flex-row space-x-3">
            <div className="w-[60px] h-[60px] rounded-full bg-gray-100 flex items-center justify-center">
                <img src={testProfileImg} alt={`safemind-user-${"username"}`} className="mx-auto "/>
            </div>
            <div>
                <h1 className="text-[18px]">Hello, <span className="font-semibold">John Doe</span></h1>
                <h3 className="text-[14px] text-black/70 mt-1">You're in a safe space.✅</h3>
            </div>
        </section>

        <section className="w-full self-center text-3xl text-gray-500 lg:order-3 lg:flex lg:justify-end lg:items-end">
            <IoMdNotificationsOutline/>
        </section>

        <section className="mt-1 w-full col-span-full lg:col-span-1 flex border border-gray-300 p-2 items-center rounded-full lg:order-2">
            <CiSearch className="w-[10%] text-lg"/>
            <input type="text" placeholder="Search here..." className="w-[90%] outline-none text-lg text-black/70 font-light"/>
        </section>
    </main>
  )
}

export default DashboardHeader