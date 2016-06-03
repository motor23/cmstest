const initialState = {
    isLoading: true,
    title: null,
    stream: null,
    items: [],
    filters: {},
    errors: {},
    total: 0,
    limit: 20,
    offset: 0
};


export default function stream(state=initialState, action={}) {
    if (action.type === 'STREAM_UPDATE_REQUEST') {
        return {
            ...initialState,
            isLoading: true
        };
    }

    if (action.type === 'STREAM_UPDATE_SUCCESS') {
        return {
            ...state,
            isLoading: false,
            title: action.payload.title,
            stream: action.payload.stream,
            items: action.payload.items,
            filters: action.payload.filters,
            errors: action.payload.errors,
            total: action.payload.total,
            limit: action.payload.limit,
            offset: action.payload.offset
        };
    }

    if (action.type === 'STREAM_UPDATE_FAILURE') {
        return {
            ...initialState,
            isLoading: false
        };
    }

    return state;
}