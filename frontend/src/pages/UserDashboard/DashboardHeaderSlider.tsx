import meditatingLadyImg from "../../assets/meditatingLady.svg"
import { FaArrowRight } from "react-icons/fa";
import LandingPgButton from "../../component/LandingPgButtonStyles/LandingPgButton";
import { Carousel } from 'antd';
import alertImg from "../../assets/boyAlertImg.svg"
import callForHelpImg from "../../assets/callHelpImg.svg"
import completeProfileImg from "../../assets/completeProfileIllustration.svg"

// import { Swiper, SwiperSlide } from 'swiper/react';

const DashboardHeaderSlider = () => {
    const sliderDatas = [
        {
            text: "You’re not alone. Every step you take toward healing matters. Get support now",
            ctaBtnText: "Daily Check-in",
            paragraph: "",
            image: meditatingLadyImg
        },
        {
            text: "Complete your profile to stay safe",
            ctaBtnText: "Continue Setup",
            paragraph: "Add your 3 emergency contact now to activate SOS help.",
            image: completeProfileImg
        },
        {
            text: "New Partner Alert!",
            ctaBtnText: "Learn More",
            paragraph: "We have teamed up with SafeCare NGO to bring faster crisis response",
            image: alertImg
        },
        {
            text: "Emergency? Don't Wait.",
            ctaBtnText: "Get help now",
            paragraph: "We have teamed up with SafeCare NGO to bring faster crisis response",
            image: callForHelpImg
        },
    ]
    return (
        <main className="my-4 bg-[url('/src/assets/dashboardSliderBgImg.png')] bg-cover bg-center h-[245px] px-6 w-full rounded-tl-[20px] rounded-br-[20px]">

            <Carousel autoplay className="">
                {sliderDatas.map((data, idx) => (
                    <div key={idx}>
                        <section className="flex items-center justify-between gap-4 px-4">
                            <div className="w-[60%] flex flex-col space-y-3">
                                <h1 className="text-[28px] font-semibold">{data.text}</h1>
                                <p className="text-lg text-black/70">{data.paragraph}</p>
                                <LandingPgButton onClick={() => console.log("kd")} className={`bg-primaryBlue-300  text-[13px] hover:opacity-70 hover:transition-all hover:duration-300 ${data.text.includes("Emergency") && "bg-transparent border-2 border-red-500 text-red-500"} text-white`}>
                                    <div className={`flex space-x-2 items-center px-5 text-lg  ${data.text.includes("Emergency") && " text-red-500"}`}>
                                        <p>{data.ctaBtnText}</p>
                                        <FaArrowRight />
                                    </div>
                                </LandingPgButton>
                            </div>
                            <div className="w-[40%] h-[245px]">
                                <img src={data.image} alt={data.ctaBtnText} />
                            </div>
                        </section>
                    </div>
                ))}
            </Carousel>

        </main>

    )
}

export default DashboardHeaderSlider