import { useState } from "react"

export const useCardSlider = (totalCards: number, visibleCardCount: number)=>{
    const [startIdx, setStartIdx] = useState<number>(0)
    // const [disableBtn, setDisableBtn] = useState<boolean>(false)



    const next = ()=>{
        // startIdx === totalCards ? setDisableBtn(true) : setDisableBtn(false)

        if(visibleCardCount + startIdx < totalCards){
            setStartIdx(startIdx + 1)
        }
    }

    const prev = ()=>{
        //Disable prev btn if startIdx = 0
        // startIdx == 0 ? setDisableBtn(true) : setDisableBtn(false)

        // go back by 1 on call of prev if startIdx > 0
        startIdx > 0 && setStartIdx(startIdx - 1)
    }

    return {next, prev, startIdx}
}