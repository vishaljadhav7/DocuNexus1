import { AppRoutes } from "./routes/routes"
import { Provider } from 'react-redux'
import { store } from "./app-store/store"

const App = () => {
  return (<>
  <Provider store={store}>
    <AppRoutes/>
  </Provider>,
  </>)
}


export default App
