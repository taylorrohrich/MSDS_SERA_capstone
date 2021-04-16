

const Button = ( props)=>{
    return <div onClick={props.onClick} style={{cursor: 'pointer', display:'flex', alignItems:'center', justifyContent: 'center', padding: 10, marginLeft:10, marginRight: 10,borderRadius:25, backgroundColor:'#232D4B',color:'white'}}>{props.children}</div>
}
export default Button