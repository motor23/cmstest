const initialState = {
    isLoading: false,
    dashboard: [],
    menu: []
};


export default function conf(state=initialState, action={}) {
    if (action.type === 'CONF_UPDATE_REQUEST') {
        return {
            ...initialState,
            isLoading: true
        };
    }

    if (action.type === 'CONF_UPDATE_SUCCESS') {
        return {
            ...state,
            isLoading: false,
            dashboard: action.payload.menu.dashboard,
            menu: action.payload.menu.main
        };
    }

    if (action.type === 'CONF_UPDATE_FAILURE') {
        return {
            ...initialState,
            isLoading: false
        };
    }

    return state;
}