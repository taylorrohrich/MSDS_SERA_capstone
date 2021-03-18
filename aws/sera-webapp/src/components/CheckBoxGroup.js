import { useState } from "react"
import ArrowRight from "../resources/arrow-right.svg"
import ArrowDown from "../resources/arrow-down.svg"
const CheckBoxGroup = (props)=>{
    const {title,items=[],onClick,collapsed=false,onToggle} = props
    const Arrow = collapsed ? ArrowRight : ArrowDown
    // const [checkBoxStates, setCheckBoxStates] = useState(new Array(items.length).fill(false));
    return <div style={{marginLeft:20,marginRight:20}}>
    <div style={{fontSize: 26, marginBottom: 10, marginTop:10, padding:10,color:"white",backgroundColor: '#E57200',display:'flex',flexDirection:'row',alignItems:'center'}}>  
    <img onClick={onToggle} src={Arrow} style={{width:25,height:25,marginRight:10,cursor:'pointer'}}/><div>{title}</div></div>
    {!collapsed ? <div style={{display:'flex', flexDirection:'row',flexWrap:"wrap",}}>
    {items.map((item,i)=><CheckBox  text={item.text} value={item.value} onClick={()=>onClick(i)}/>)}
    </div> : <div/>}
    </div>
}

const CheckBox = (props)=>{
    const {text, value, onClick} = props
    return <div style={{margin: 5,flex:1,flexBasis:"18%"}}>
        <div style={{fontWeight:'bold'}}>{text}</div>
        <input style={{margin:0}} type="checkbox" checked={value} onClick={onClick}/>
    </div>
}

export default CheckBoxGroup

