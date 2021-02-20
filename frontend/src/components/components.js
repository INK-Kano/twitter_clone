import React, { useState, useEffect } from "react";
import axios from "axios";

export const TweetsComponent = (props) => {
    const textAreaRef = React.createRef()

    const [newTweets, setNewTweets] = useState([])

    const handleSubmit = (event) => {
        event.preventDefault();

        const newVal = textAreaRef.current.value
        let tempNewTweets = [...newTweets]

        tempNewTweets.unshift({
            content: newVal,
            likes: 0,
            id: 123
        })
        setNewTweets(tempNewTweets)

        textAreaRef.current.value = ''
    };

    return (
        <div className={props.className}>
            <div className="col-12">
                <form onSubmit={handleSubmit}>
                    <textarea ref={textAreaRef} required={true} className="form-control" name="tweet">

                    </textarea>
                    <button className="btn btn-primary my-3" type="submit">
                        Tweet
                    </button>
                </form>
            </div>
            <TweetsList newTweets={newTweets} />
        </div>
    );
};

export const ActionBtn = (props) => {
    const { tweet, action } = props;

    const [likes, setLikes] = useState(tweet.likes ? tweet.likes : 0);
    const [userLike, setUserLike] = useState(tweet.userLike === true ? true : false);

    const className = props.className ? props.className : "btn btn-primary btn-sm";

    // this ${} has to be with `
    const display =
        action.type === "like" ? `${likes} ${action.display}` : action.display;

    const handleClick = (event) => {
        event.preventDefault();

        if (action.type === "like") {
            if (userLike === true) {
                setLikes(likes - 1);
                setUserLike(false);
            } else {
                setLikes(likes + 1);
                setUserLike(true);
            }
        }
    };

    return (
        <button className={className} onClick={handleClick}>
            {display}
        </button>
    );
};

export const Tweet = (props) => {
    const { tweet } = props;
    const className = props.className
        ? props.className
        : "col-10 mx-auto col-md-6";

    return (
        <div className={className}>
            <p>
                {tweet.id} - {tweet.content}
            </p>
            <div className="btn btn-group">
                <ActionBtn
                    tweet={tweet}
                    action={{ type: "like", display: "Likes" }}
                />
                <ActionBtn
                    tweet={tweet}
                    action={{ type: "unlike", display: "Unlike" }}
                />
                <ActionBtn
                    tweet={tweet}
                    action={{ type: "retweet", display: "Retweet" }}
                />
            </div>
        </div>
    );
};

export const TweetsList = (props) => {
    const [tweetsInit, setTweetsInit] = useState([]);
    const [tweets, setTweets] = useState([]);

    useEffect(() => {
        const final = [...props.newTweets].concat(tweetsInit)
        console.log(final)
        if (final.length !== tweets.length) {
            setTweets(final)
        }
        
    }, [props.newTweets, tweets, tweetsInit]);

    useEffect(() => {
        const loadTweets = async () => {
            const url = "http://localhost:8000/api/tweets/";
            await axios
                .get(url)
                .then(function(response) {
                    setTweetsInit(response.data);
                })
                .catch(function(error) {
                    alert(error);
                });
        };

        loadTweets();
    }, []);

    return tweets.map((tweet, index) => {
        return (
            <Tweet
                tweet={tweet}
                key={index}
                className="my-5 p-5 border bg-white text-dark pd-5"
            />
        );
    });
};
