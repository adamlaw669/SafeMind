import Footer from "../../component/footer/Footer"
import NavBar from "../../component/Navbar/NavBar"
import CTA from "./CTA"
import HowItWorks from "./HowItWorks"
import LandingHeader from "./LandingHeader"


const Landing = () => {
  return (
    <main>
      <NavBar />

      <section className="">
        <div className="px-6 pt-20 md:px-16">
          <LandingHeader />
        </div>
        <div className="px-6 pt-20 md:px-16 py-6 bg-[#F2F9FF]">
          <HowItWorks />
        </div>

        <div className="px-6 pt-20 md:px-16 py-6">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officia ab ipsum fugiat neque? Dolores numquam molestiae quo dolore quibusdam similique at distinctio placeat, nemo error illo pariatur suscipit exercitationem neque explicabo. Doloribus, rerum? Ipsam eos rem neque sequi quos? Adipisci soluta necessitatibus reiciendis facere quam qui amet illo deleniti, voluptatibus temporibus blanditiis, nulla magni veniam vel. Atque quisquam enim libero natus unde aut necessitatibus cum? Nemo tempore quod quae laboriosam, rerum molestiae laborum quos quis perferendis itaque reiciendis eos voluptatibus quam officiis sunt veniam recusandae! Aliquid eius praesentium nihil, dicta voluptatum ea earum inventore beatae accusamus aliquam similique assumenda nesciunt.
        </div>

        <div className="bg-[#F2F9FF]">
          <CTA />
        </div>

      </section>
    </main>
  )
}

export default Landing