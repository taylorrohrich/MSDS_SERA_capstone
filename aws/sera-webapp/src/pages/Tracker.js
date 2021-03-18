import { useState,useEffect } from "react"
import {Table} from "../components"
import {api_request} from "../utils"
import {TRACKER_COLUMNS} from "../constants"

const COLUMNS=['a','b','c','d']
const ROWS = [1,2,3,4,5,6,7,8,9,10].map(item => COLUMNS)

const getTrackerInfo = (callback)=>{
  api_request('TRACKER').then(
    res=> {
      const data = res?.data
      const parsedData = Object.values(data).map(row=>
      Object.values(row)
      )
      callback(parsedData)
    }
  )
}
const Tracker = ()=>{
  const [trackerInfo,setTrackerInfo]= useState([])
  useEffect(()=>getTrackerInfo(setTrackerInfo),[])
  console.log(trackerInfo)
  return <div>
    <Table columns={TRACKER_COLUMNS.map(col=>col.split('_').join(' '))} rows={trackerInfo}/>
  </div>
}
export default Tracker;
