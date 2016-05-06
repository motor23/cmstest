import Application from './components/application';
import Dashboard from './components/dashboard';
import Login from './components/login';
import Stream from './components/stream';
import StreamList from './components/stream-list';
import StreamItem from './components/stream-item';


export default function configureRoutes() {
    return {
        path: '/',
        component: Application,
        indexRoute: {component: Dashboard},
        childRoutes: [
            {
                path: ':stream',
                component: Stream,
                indexRoute: {component: StreamList},
                childRoutes: [
                    {
                        path: ':id',
                        component: StreamItem
                    }
                ]
            }
        ]
    }
}