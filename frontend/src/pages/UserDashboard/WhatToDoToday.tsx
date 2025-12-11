import { MdHealthAndSafety } from "react-icons/md";
import { ImFolderOpen } from "react-icons/im";
import { FaEarthAmericas } from "react-icons/fa6";
import { FaArrowRight } from "react-icons/fa";
import warningSign from "../../assets/warningSigm.svg"
import { useState } from "react";
import ModalForContent from "./ModalsForContent/ModalForContent";


const WhatToDoToday = () => {
    const [togglePopup, setTogglePopup] = useState<boolean>(false)
    const [popupName, setPopupName] = useState<string>("")

    const datas = [
        {
            text: "Report an incident",
            paragraph: "Share safely and securely",
            icon: <MdHealthAndSafety />,
            bgColor: "bg-[#EFF0F8]",
            popupType: "report",
        },
        {
            text: "Track my Cases",
            paragraph: "Monitor your report progress",
            icon: <ImFolderOpen />,
            bgColor: "bg-[#EFFCFF]",
            popupType: "track",
        },
        {
            text: "Find support",
            paragraph: "Connect with verified helpers",
            icon: <FaEarthAmericas />,
            bgColor: "bg-[#FCF7FF]",
            popupType: "support",
        },
    ]

    

    const handleModal = (popupType: string) => {
        setPopupName(popupType)
        setTogglePopup(true)
        
    }

    return (
        <main className='py-5'>
            {togglePopup && <ModalForContent popupType={popupName} togglePopup={togglePopup} closePopup={()=>setTogglePopup(false)}/>}

            <h1 className="text-[24px] font-semibold pb-6">What would you like to do today?</h1>

            <section className="grid grid-cols-3 gap-4">
                {datas.map((data, idx) => (
                    
                    <div key={idx} className={`flex flex-col items-center justify-center space-y-1 ${data.bgColor} p-4 rounded-[16px] shadow-md cursor-pointer hover:-translate-y-0.5 hover:transition-all hover:duration-300`} onClick={()=>handleModal(data.popupType)}>
                        <span className="text-6xl text-primaryBlue-300">{data.icon}</span>
                        <h2 className="pt-2 text-[24px] font-semibold">{data.text}</h2>
                        <p className="text-[16px] text-black/70">{data.paragraph}</p>

                        <FaArrowRight className="self-end mt-2" />
                    </div>
                ))}
            </section>

            <section className="my-6 bg-[#FFF0F0] px-8 w-full rounded-full py-3 items-center flex flex-row justify-between">
                <div className="flex space-x-2 items-center">
                    <img src={warningSign} alt="need help?" className="" />
                    <h2 className="font-semibold text-[15px]">Need Urgent Help? Call a trusted NGO or emergency line now</h2>
                </div>
                <button className="bg-[#F44336] px-5 text-[14px] font-semibold py-2 rounded-full hover:opacity-80 cursor-pointer text-white">Contact Now</button>
            </section>
        </main>
    )
}

export default WhatToDoToday