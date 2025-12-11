import DashboardNav from "../../component/dashboardNav/DashboardNav"
import CommunityPreview from "./CommunityPreview"
import DashboardHeader from "./DashboardHeader"
import DashboardHeaderSlider from "./DashboardHeaderSlider"
import WhatToDoToday from "./WhatToDoToday"

const AgencyDashboard = () => {
  return (
    <main className="w-full flex flex-col lg:flex-row">
      <section className="w-full lg:max-w-[300px]">
        <DashboardNav />
      </section>

      <section className="w-full mt-20 px-4 lg:mt-4 lg:px-8 lg:py-8 lg:max-w-[calc(100%-300px)]">
        <DashboardHeader />
        <DashboardHeaderSlider />
        <WhatToDoToday/>
        <CommunityPreview/>
      </section>

    </main>
  )
}

export default AgencyDashboard