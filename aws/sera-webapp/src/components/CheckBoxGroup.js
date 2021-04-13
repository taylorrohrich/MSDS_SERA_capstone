import { useState } from "react"
import ArrowRight from "../resources/arrow-right.svg"
import ArrowDown from "../resources/arrow-down.svg"
import { Multiselect } from 'multiselect-react-dropdown';
const CheckBoxGroup = (props)=>{
    const {title,items=[],labels=[],onClick,collapsed=false,onToggle,isDropdown=false} = props
    const Arrow = collapsed ? ArrowRight : ArrowDown
    return <div style={{marginLeft:20,marginRight:20}}>
    <div style={{fontSize: 26, marginBottom: 10, marginTop:10, padding:10,color:"white",backgroundColor: '#E57200',display:'flex',flexDirection:'row',alignItems:'center'}}>  
    <img onClick={onToggle} src={Arrow} style={{width:25,height:25,marginRight:10,cursor:'pointer'}}/><div>{title}</div></div>
    {!collapsed ? <div style={{display:'flex', flexDirection:'row',flexWrap:"wrap",}}>
        {
            isDropdown ?  <Multiselect
            options={items.map((item,index)=>({name:item.text, id:index}))} // Options to display in the dropdown
            onSelect={(_,item)=>onClick(item.id)} // Function will trigger on select event
            onRemove={(_,item)=>onClick(item.id)} // Function will trigger on remove event
            displayValue="name" // Property name to display in the dropdown options
            /> :    items.map((item,i)=><CheckBox  text={item.text} label={labels?.[i]} value={item.value} onClick={()=>onClick(i)}/>)
        }
    </div> : <div/>}
    </div>
}

const CheckBox = (props)=>{
    const {text, value, onClick,label} = props
    return <div style={{margin: 5,flex:1,flexBasis:"18%"}}>
        <div style={{fontWeight:'bold'}}>{label || text}</div>
        <input style={{margin:0}} type="checkbox" checked={value} onClick={onClick}/>
    </div>
}

export default CheckBoxGroup

