const initialState = {
    navigation: [],
    dashboard: []
};


export function config(state=initialState, action={}) {
    switch (action.type) {
        case 'CONFIG_UPDATE':
            return Object.assign({}, state, {
                navigation: action.payload.navigation,
                dashboard: action.payload.dashboard
            });
    }
    return state;
}