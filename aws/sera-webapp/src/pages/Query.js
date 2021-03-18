import { useState } from "react"
import {CheckBoxGroup} from "../components"
import {QUERY_FIELDS} from "../constants"
import {api_request} from "../utils"


//const generateCheckBoxGroups = (itemsGroup)=> itemsGroup.map(items => <CheckBoxGroup items={groupOne} onClick={(index)=>setGroupOne(switchItem(groupOne,index))}/>)
const parseItems = (items)=> {
    return items.reduce((acc,item)=>{
        return {...acc, [item.type]: {...item,values: item.values.map(obj=>({text:obj,value:false}))}}
        },{})
}


const switchItem = (items,index,type)=>{
    const curItem = items[type]
    const x= {...items, [type]: {...curItem,values: [...curItem.values.slice(0,index),{...curItem.values[index],value: !curItem.values[index].value},...curItem.values.slice(index+1)]}}
    return x
}

const submitQuery=(itemsGroups)=>{
    const selectedVals = Object.keys(itemsGroups).reduce((acc,key)=>{
        const selectedValues = itemsGroups[key].values.filter(val=>val.value).map(val=>val.text).join(',')
        if (!selectedValues.length) return acc
        if (key.includes('specific')){
            if (acc['specific_measure_list']){
                return  {...acc,'specific_measure_list':[acc['specific_measure_list'],selectedValues].join(',')}
            }else{
                return  {...acc,'specific_measure_list':selectedValues}
            }
        }
        return  {...acc,[key]:selectedValues}
    },{})
    api_request("CSV",selectedVals)
}
const Query = ()=>{
const [itemsGroups,setItemsGroups] = useState(parseItems(QUERY_FIELDS))
const [collapsed,setCollapsed] = useState([false,false,false,false,true,true,true,true])
return <div style={{marginTop:20}}>
    <div style={{margin:20,fontSize:32,paddingLeft:20}}>Query</div>
    <div>
    {Object.keys(itemsGroups).map((key,index)=> <CheckBoxGroup onToggle={()=>setCollapsed([...collapsed.slice(0,index),!collapsed[index],...collapsed.slice(index+1)])
    }collapsed={collapsed[index]} title = {itemsGroups[key].label} items={itemsGroups[key].values} onClick={(index)=>setItemsGroups(switchItem(itemsGroups,index,key))}/>)}
</div>
<div style={{display:'flex',cursor:'pointer',justifyContent:'center',alignItems:'center',margin:20}}>
    <div onClick={()=>submitQuery(itemsGroups)}style={{color:'white',backgroundColor:'#232D4B', padding: 10,paddingLeft: 20,paddingRight:20,borderRadius:25}}>Submit</div>
    </div>
</div>

}
export default Query;
