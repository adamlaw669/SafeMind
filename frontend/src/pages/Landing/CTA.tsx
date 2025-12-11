import ctaImg from "../../assets/sosImg.svg"
import LandingPgButton from "../../component/LandingPgButtonStyles/LandingPgButton"
import emergencySymbol from "../../assets/emergencySymbol.svg"

const CTA = () => {
    return (
        <main className='flex items-center '>
            <section className="px-6 pt-20 md:px-16 py-6 flex flex-col space-y-6">
                <h1 className="text-4xl text-center font-semibold">Need Help Right Now?</h1>
                <p className="text-center text-lg mx-auto">If you're in danger or feel unsafe, you can quickly alert trusted contacts &mdash; even without logging in.</p>
                <LandingPgButton className="bg-[#FF3C3C] px-8 py-2 mx-auto hover:opacity-80" onClick={() => { }}>
                    <div className="flex items-center space-x-2 ">
                        <p className=" text-white">Send emergency alert</p>
                        <img src={emergencySymbol} alt="emergency" />
                    </div>
                </LandingPgButton>
            </section>

            <section className="w-[80%]">
                <img src={ctaImg} alt="Need help right now?" />
            </section>
        </main>
    )
}

export default CTA