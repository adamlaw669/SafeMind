import tellYourStoryImg from "../../assets/tellYourStoryImg.svg"
import getMatchedImg from "../../assets/getMatchedImg.svg"
import takeActionImg from "../../assets/takeActionImg.svg"
import rebuildImg from "../../assets/rebuild&growImg.svg"


type DatasType = {
    img:string;
    header:string;
    bodyText: string;
}
const datas: DatasType[] = [
    {
        img: tellYourStoryImg,
        header: "Tell your story",
        bodyText: "Share your experience safely and anonymously — no pressure, no judgement."
    },
    {
        img: getMatchedImg,
        header: "Get Matched",
        bodyText: "We connect you with trusted helpers who truly understand and care."
    },
    {
        img: takeActionImg,
        header: "Take Action",
        bodyText: "Receive guidance or emergency help tailored to your situation."
    },
    {
        img: rebuildImg,
        header: "Rebuild & Grow",
        bodyText: "Find healing, strength, and confidence to move forward — at your own pace."
    },
]


const HowItWorks = () => {
  return (
    <main className=''>
        <section className="px-14 md:w-[70%] rounded-l-full bg-primaryBlue-300 py-4 place-self-end">
            <h2 className="text-white text-xl md:text-2xl font-semibold">How SafeMind Works</h2>
            <p className="font-light text-white/60 mt-1 text-[14px]">Your safety journey, one step at a time👌</p>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
            {
                datas.map((data, idx)=>(
                    <div key={idx} className="bg-white rounded-lg shadow-2xl flex flex-col space-y-3 items-center p-3 hover:scale-105 hover:transition-all hover:duration-300">
                        <img src={data.img} alt={`${data.header}`} className=" h-36"/>
                        <h2 className="font-semibold text-xl mt-4">{data.header}</h2>
                        <p className="text-black/80 text-center">{data.bodyText}</p>
                    </div>
                ))
            }
        </section>
    </main>
  )
}

export default HowItWorks