const initialState = {
    isConnected: false,
    shouldReloadPage: false
};


export default function app(state=initialState, action={}) {
    switch (action.type) {
        case 'APP_CONNECTION_REQUEST':
            return {
                ...initialState,
                isConnected: false
            };

        case 'APP_CONNECTION_CLOSED':
            return {
                ...initialState,
                isConnected: false,
                shouldReloadPage: action.payload.shouldReloadPage
            };

        case 'APP_CONNECTION_OPENED':
            return {
                ...initialState,
                isConnected: true
            };
    }
    return state;
}