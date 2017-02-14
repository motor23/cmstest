const initialState = {
    hash: '',
    key: '',
    pathname: '',
    search: ''
};


export function routing(state=initialState, action={}) {
    switch (action.type) {
        case 'PUSH':
        case 'REPLACE':
            return action.payload;
    }
    return state;
}