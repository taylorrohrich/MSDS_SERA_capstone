import axios from 'axios'
import {API_ENDPOINT,ROUTES} from "../constants"
const api_request = async (endpoint,data)=>{
    const route = ROUTES[endpoint]
    const {path,parameters} = route
    const params = parameters.reduce((acc,param)=>{
        if (data[param]){
            return {...acc,[param]:data[param]}
        }
        return acc
    },{})
    return axios.get(`${API_ENDPOINT}${path}`, {
        params
      })
      .then(response=> {
        console.log(response);
        if (response?.headers?.['content-type']==='text/csv'){
          const blob = new Blob([response.data], { type: 'text/csv' })
          const url = window.URL.createObjectURL(blob)
          window.open(url)
        }else{
          return response
        }
 // Mostly the same, I was just experimenting with different approaches, tried link.click, iframe and other solutions
      })
}

export {api_request}