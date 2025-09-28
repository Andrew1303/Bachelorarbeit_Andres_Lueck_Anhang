import DataoverwatchCSS from './dataoverwatch.module.css'
import jsonfile from '../../data/V3_202508210559_al-1_ap-330_it-4_temp-0.2_202508210024_Prompts_2_Dic_Qwen3-Embedding-8B_MIL-HDBK-217F_BFRS_Version1_pagechunk_V1.json'
import { useState, useEffect } from 'react'
import axios from 'axios';
// import { IconType } from 'react-icons';
import { BsChevronCompactLeft, BsChevronCompactRight, BsCaretLeftFill, BsCaretRightFill, BsFillSave2Fill, BsCheck2, BsXLg } from "react-icons/bs";
// type HomepageProps = {
//   name : string
// }

// type Props = {
//   Icon: IconType;
// };

// (parameter) item: {
//     model: string;
//     language: string;
//     prompt: string;
//     itemname: string;
//     expectedbfr: number[];
//     context: string;
//     results: {
//         duration: number[];
//         answer: string[];
//         found_bfrs: number[][];
//         correct_context: boolean
//     };
// }


export default function Dataoverwatch(){
    let [ItemID, setItemID] = useState<number>(0)
    let [SelectionItemID, setSelectionItemID] = useState<string>(String(ItemID+1))
    let [Value, setValue] = useState<number>(0)
    let [data, setdata] = useState(jsonfile)
    let [ResultsList, setResultlist] = useState<any>([])
    let [selectedResult, setSelectedResult] = useState<string>('')

    // --------- INIT ---------
    useEffect(() => {
        const getResultList = async() => {
            try{
                const response = await axios.get<any>("http://localhost:8000/resultList")
                setResultlist(response.data)
                console.log(response.data)
            } catch (err) {
                console.log("An error has occured!\n", err)
            }
        }
        getResultList()
    }, [])

    // ------ FUNCTIONS -------
    const saveData = async(results:any, filename:string) => {
        // try{
        //     const response = await axios.get<any>("http://localhost:8000/resultList")
        //     console.log(response)
        // } catch(err) {

        // }
        let formData = new FormData();

        formData.append("results", JSON.stringify(results));
        formData.append("filename", filename);

        console.log(JSON.stringify(results))
        try{
            await axios({
                method: "post",
                url: "http://localhost:8000/saveResult",
                data: formData,
                headers: { "Content-Type": "multipart/form-data" },
            }).then(response => {
                console.log("Success")
            })
        }
        catch(error) {
            console.error("An error has occured!", error)
        } 

            // axios.post('http://localhost:8000/save', {
            //     formData
            // })
            // .then(response => {
            // console.log('Saved:', response.data);
            // })
            // .catch(error => {
            // console.error('Error:', error);
            // });
    }

    const changeFile = async(filename:string) => {
        try{
            const response = await axios.get<any>(
                "http://localhost:8000/getResult",
                {
                    params:{
                        filename: filename
                    }
                }
            )
            console.log(response.data)
            setValue(0)
            setItemID(0)
            setSelectionItemID("1")
            setdata(response.data)
            setSelectedResult(filename)
        } catch (err){
            console.log("An error has occured!\n", err)
        }
    }

    const changeContextJudgement = (judgement:string) => {
        let updatedData = [...data]
        updatedData[ItemID].goodcontext = judgement
        setdata(updatedData)
    }

    return(
        <div className={DataoverwatchCSS.mainbox}>
            <div className={DataoverwatchCSS.navbox}>
                <select className={DataoverwatchCSS.Selection} onChange={(e) => changeFile(e.target.value)}>
                    {ResultsList.map((item:string, index:number) => {
                        return(
                            <option value={item}>{index+1}. {item}</option>
                        )
                    })}
                </select>
                <div className={DataoverwatchCSS.promptbox}>
                    <p>{data[ItemID].prompt}</p>
                </div>
                <div className={DataoverwatchCSS.navoptionbox}>
                    <BsFillSave2Fill className={DataoverwatchCSS.savebtn} onClick={() => saveData(data, selectedResult)}/>
                    <p><input className={DataoverwatchCSS.inputfield} value={SelectionItemID} onChange={(e) => setSelectionItemID(e.target.value)} onKeyDown={(e) => {if (e.key === "Enter" && Number((e.target as HTMLInputElement).value) > 0 && Number((e.target as HTMLInputElement).value) < (data.length + 1)){setItemID(Number((e.target as HTMLInputElement).value)-1)}}}/>/{data.length}</p>  
                </div>     
            </div>
            <div className={DataoverwatchCSS.contentbox}>
                <div className={DataoverwatchCSS.leftbox}>
                    <button className={DataoverwatchCSS.itembtn_left} onClick={() => (ItemID === 0 ? (setItemID(data.length - 1), setSelectionItemID(String(data.length))) : (setItemID(ItemID -= 1), setSelectionItemID(String(ItemID + 1))), setValue(0))}><BsChevronCompactLeft size={72} color="white"/></button>
                </div>
                <div className={DataoverwatchCSS.corebox}>
                    <div className={DataoverwatchCSS.topleftbox}>
                        <div className={DataoverwatchCSS.titlebox}>
                            <h2>Final Answer</h2>
                        </div>
                        <div className={DataoverwatchCSS.subcontentbox}>
                            <p style={{whiteSpace: 'pre-wrap'}}>{data[ItemID].results.answer[Value]}</p>
                        </div>
                        {/* <textarea className={DataoverwatchCSS.Fullusage} value={data[ItemID].results.answer[Value]}/> */}
                    </div>
                    <div className={DataoverwatchCSS.toprightbox}>
                        <div className={DataoverwatchCSS.titlebox}>
                            <h2>First Answer</h2>
                        </div>
                        <div className={DataoverwatchCSS.subcontentbox}>
                            <p style={{whiteSpace: 'pre-wrap'}}>{data[ItemID].results.firstanswers[Value]}</p>
                        </div>     
                    </div>
                    <div className={DataoverwatchCSS.bottomleftbox}>
                        <div className={DataoverwatchCSS.titlebox}>
                            <h2>Basefailurerate</h2>
                        </div>
                        <div className={DataoverwatchCSS.subcontentbox}>
                            <ul>
                                {data[ItemID].results.found_bfrs[Value].map((item, index) => {
                                    let fontcolor = ''
                                    if (data[ItemID].expectedbfr.includes(item)){
                                        fontcolor = 'green'
                                    } else{
                                        fontcolor = 'red'
                                    }
                                    return(
                                        <li style={{color: fontcolor}}>
                                            {item}
                                        </li>
                                    )

                                })}
                            </ul>
                        </div>
                    </div>
                    <div className={DataoverwatchCSS.bottomrightbox}>
                        <div className={DataoverwatchCSS.titlebox}>
                            <h2>Context</h2>
                        </div>
                        <div className={DataoverwatchCSS.subcontentbox}>
                            <p style={{whiteSpace: 'pre-wrap'}}>{data[ItemID].context}</p>
                        </div>
                    </div>
                    {/* <ul>
                        {data.map((item, index) => (
                            <li key={index}>
                                <strong>{item.model}</strong>: {item.prompt}
                            </li>
                        ))}
                    </ul> */}
                    
                </div>
                <div className={DataoverwatchCSS.rightbox}>
                    <button className={DataoverwatchCSS.itembtn_right} onClick={() => (ItemID === (data.length -1) ? (setItemID(0), setSelectionItemID(String(1))) : (setItemID(ItemID += 1), setSelectionItemID(String(ItemID + 1))), setValue(0)) }><BsChevronCompactRight size={72} color="white"/></button>
                </div>
            </div>
            <div className={DataoverwatchCSS.navigationbox}>
                <div className={DataoverwatchCSS.buttonbox}>
                    <BsCaretLeftFill className={DataoverwatchCSS.switchbtn} onClick={() => (Value === 0 ? setValue(data[ItemID].results.answer.length - 1): setValue(Value -= 1))}/>
                    <p>{Value+1}/{data[ItemID].results.answer.length}</p>
                    <BsCaretRightFill className={DataoverwatchCSS.switchbtn} onClick={() => (Value === (data[ItemID].results.answer.length - 1) ? setValue(0): setValue(Value += 1))}/>
                </div>
                <div className={DataoverwatchCSS.ContextJudgementBox}>
                    <p>Context:</p>
                    <button className={DataoverwatchCSS.ContextBtn} style={{backgroundColor: data[ItemID].goodcontext === "good" ? 'rgba(37, 221, 0, 1)': 'rgb(161, 161, 180)'}} onClick={() => changeContextJudgement("good")}><BsCheck2 style={{width: "55%", height: "55%"}}/></button>
                    <button className={DataoverwatchCSS.ContextBtn} style={{backgroundColor: data[ItemID].goodcontext === "bad" ? 'red': 'rgb(161, 161, 180)'}} onClick={() => changeContextJudgement("bad")}><BsXLg style={{width: "55%", height: "55%"}}/></button>
                </div>
                <div className={DataoverwatchCSS.clickerbox}>
                </div>
            </div>
        </div>
  )
}