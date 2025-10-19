import {
	Text,
	TextInput,
	View,
	StyleSheet,
	NativeSyntheticEvent,
	TextInputSubmitEditingEventData,
	Animated,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { storeData, getStreamURL } from "@/utils/localStorage";
import { useEffect, useState, useRef } from "react";
// import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { Router, useRouter } from "expo-router";

export default function Index() {
	const router = useRouter();
	const [text, setText] = useState<string>();
	const [isLoaded, setIsLoaded] = useState<boolean>(false);

	//page fade animation values
	const fadeInAnim = useRef(new Animated.Value(0)).current;
	// const fadeOutAnim = useRef(new Animated.Value(1)).current;
	useEffect(() => {
		const loadPreviousURL = async () => {
			try {
				const existingUrl = await getStreamURL();

				if (existingUrl) {
					setText(existingUrl);
				} else {
					setText("");
				}
			} catch (e) {
				console.log(e);
			} finally {
				setIsLoaded(true);
			}
		};
		loadPreviousURL();
	}, []);

	useEffect(() => {
		if (isLoaded) {
			Animated.timing(fadeInAnim, {
				toValue: 1,
				duration: 1000,
				useNativeDriver: true,
			}).start();
		}
	}, [isLoaded, fadeInAnim]);

	if (isLoaded) {
		//grab url, if it is null text is undefined.
		return (
			<View
				style={{
					flex: 1,
					justifyContent: "center",
					alignItems: "center",
					// 	backgroundColor: "#5bbde1ff",
				}}
			>
				<LinearGradient
					colors={["#3d6d80ff", "#074a5cff", "#074a5cff", "#3c7e98ff"]}
					locations={[0, 0.3, 0.8, 1]}
					start={{ x: 0.5, y: 0 }}
					end={{ x: 0.5, y: 1 }}
					style={styles.gradient}
				>
					<Animated.View
						style={{
							flex: 1,
							// justifyContent: "center",
							alignItems: "center",
							opacity: fadeInAnim,
							width: "100%",
						}}
					>
						<View
							style={{
								width: "65%",
								alignItems: "center",
								paddingBottom: "15%",
								paddingTop: "70%",
							}}
						>
							<Text style={styles.h1}>Poolside</Text>
							<Text style={styles.slogan}>
								Using Computer Vision to Make Pools Safer for Your Kids.
							</Text>
						</View>
						<TextInput
							style={styles.inputBox}
							defaultValue={text}
							placeholder="type your RTSP/ stream URL"
							onSubmitEditing={(event) => handleRTSPInput(event, router)}
						></TextInput>
					</Animated.View>
				</LinearGradient>
			</View>
		);
	}

	return (
		<>
			<Text>Loading...</Text>
		</>
	);
}

const handleRTSPInput = async (
	event: NativeSyntheticEvent<TextInputSubmitEditingEventData>,
	router: Router
) => {
	const text = event.nativeEvent.text;
	const payload = {
		// mode: "cors",
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ streamURL: text }),
	};
	await fetch("http://10.0.0.119:5000/get-stream-url", payload)
		.then((response) => console.log(response))
		.catch((error) => console.log(error));
	await storeData(text);
	console.log("go to next page");
	if (text) router.push("./video-preview");
	//we might want to add here a validator to make sure we actually can establish a connection
	//before navigating to the next route. We might render an error on the page
	//if the user input is an invalid stream address
	//another option is to first route to a loading screen to establisht eh connection and then route
	//to the video preview
};

const styles = StyleSheet.create({
	inputBox: {
		backgroundColor: "rgba(249, 249, 249, 0.8)",
		borderColor: "black",
		borderWidth: 0.5,
		borderRadius: 10,
		paddingLeft: 10,
		paddingRight: 10,
		height: 50,
		width: "60%",
		fontSize: 12,
		shadowColor: "#000",
		shadowOffset: { width: 0, height: 2 },
		shadowOpacity: 0.25,
		shadowRadius: 3.84,
	},
	h1: {
		fontSize: 60,
		fontWeight: "bold",
		fontFamily: "System",
		color: "white",
	},
	gradient: {
		flex: 1,
		alignItems: "center",
		justifyContent: "center",
		width: "100%",
	},
	slogan: {
		color: "white",
		fontFamily: "Arial",
		fontSize: 18,
		fontWeight: "400",
		textAlign: "left",
		lineHeight: 24,
		maxWidth: "80%",
		alignSelf: "flex-start",
		paddingLeft: "5%",
		paddingRight: "5%",
	},
});
