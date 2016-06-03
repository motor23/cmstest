const initialState = {
    isConnecting: false,
    isConnected: false
};


export default function app(state=initialState, action={}) {
    switch (action.type) {
        case 'APP_CONNECTION_REQUEST':
            return {
                ...state,
                isConnecting: true,
                isConnected: false
            };

        case 'APP_CONNECTION_CLOSED':
            return {
                ...state,
                isConnecting: true,
                isConnected: false
            };

        case 'APP_CONNECTION_OPENED':
            return {
                ...state,
                isConnecting: false,
                isConnected: true
            };

        return state;
    }
}