import { FaArrowLeft } from "react-icons/fa6";
import { FaArrowRight, FaUser } from "react-icons/fa";
import DashboardCard from "../../component/dashboardCards.tsx/DashboardCard";
import communityUserDemoPreview from "../../assets/communityUserDemoPreview.svg"
import { useCardSlider } from "../../hooks/useCardSlider";
import { motion, useScroll } from "motion/react"


const CommunityPreview = () => {
  const communityDatas = [
    {
      profileImg: communityUserDemoPreview,
      title: "Healing & Recovery",
      desc: "A safe space for survivors to share, learn, and rebuild.",
      totalCommunityMembers: 130,
      fewUsersPreview: [
        {
          userProfileIng: communityUserDemoPreview
        },
        {
          userProfileIng: communityUserDemoPreview
        },
        {
          userProfileIng: communityUserDemoPreview
        },
      ]
    },
    {
      profileImg: communityUserDemoPreview,
      title: "Women's Support Circle",
      desc: "Empowering women through shared experiences and support",
      totalCommunityMembers: 273,
      fewUsersPreview: [
        {
          userProfileIng: communityUserDemoPreview
        },
        {
          userProfileIng: communityUserDemoPreview
        },
        {
          userProfileIng: communityUserDemoPreview
        },
      ]
    },
    {
      profileImg: communityUserDemoPreview,
      title: "Legal Advice Community",
      desc: "Connect with people discussing rights, options, and legal steps",
      totalCommunityMembers: 90,
      fewUsersPreview: [
        {
          userProfileIng: communityUserDemoPreview
        },
        {
          userProfileIng: communityUserDemoPreview
        },
        {
          userProfileIng: communityUserDemoPreview
        },
      ]
    },
    {
      profileImg: communityUserDemoPreview,
      title: "Men Healing Center",
      desc: "Support for men against physical and spiritual abuse",
      totalCommunityMembers: 841,
      fewUsersPreview: [
        {
          userProfileIng: communityUserDemoPreview
        },
        {
          userProfileIng: communityUserDemoPreview
        },
        {
          userProfileIng: communityUserDemoPreview
        },
      ]
    },
  ]


  const visibleCardCount = 3
  const { next, prev, startIdx } = useCardSlider(communityDatas.length, visibleCardCount)

  return (
    <main>
      <section className="flex justify-between items-center text-[24px] font-semibold mb-6">
        <h1>Your Communities</h1>

        <div className="flex space-x-3">
          <button onClick={() => prev()} className="p-3 rounded-full bg-white shadow-lg text-primaryBlue-300 cursor-pointer hover:opacity-80 text-[17px] disabled:opacity-50 disabled:cursor-not-allowed" disabled={startIdx === 0 && true}><FaArrowLeft /></button>
          <button onClick={() => next()} className="p-3 rounded-full bg-white shadow-lg text-primaryBlue-300 cursor-pointer hover:opacity-80 text-[17px] disabled:opacity-50 disabled:cursor-not-allowed" disabled={startIdx + visibleCardCount === communityDatas.length && true}><FaArrowRight /></button>
        </div>
      </section>

      <section className="grid grid-cols-3 gap-4">
        {communityDatas.slice(startIdx, startIdx + visibleCardCount).map((data, idx) => (
          <DashboardCard key={idx}>
            <div className="flex flex-col space-y-2">
              <img src={data.profileImg} alt={data.title + "profile image"} className="w-15 h-15" />
              <h2 className="text-[24px] font-semibold">{data.title}</h2>
              <p className="text-[18px] text-black/70">{data.desc}</p>

              <div className="flex flex-row justify-between items-center mt-3">
                <div className="flex -space-x-2 items-center">
                  {data.fewUsersPreview.map((user, idx) => (

                    <span className="" key={idx}>
                      <img src={user.userProfileIng} alt="" className="w-10 h-10" />
                    </span>
                  ))}
                  <span className="w-9 h-9 bg-primaryBlue-300 rounded-full flex items-center justify-center text-center text-white font-semibold">
                    <p className="text-[12px]">+{data.totalCommunityMembers - 3}</p>
                  </span>
                </div>

                <button className="px-5 py-1 cursor-pointer bg-[#F1F1F6] text-primaryBlue-300 rounded-full hover:opacity-80">View</button>
              </div>
            </div>
          </DashboardCard>
        ))}
      </section>
    </main>
  )
}

export default CommunityPreview