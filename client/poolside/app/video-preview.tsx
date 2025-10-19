import React, { useState, useEffect } from "react";
import { View, Image, StyleSheet, Text, ImageBackground } from "react-native";
import AlertBox from "@/components/AlertBox";

export default function VideoPreview() {
	const [frameUri, setFrameUri] = useState<string | null>(null);

	useEffect(() => {
		const ws = new WebSocket("ws://10.113.114.118:8888");

		
		ws.onopen = () => console.log("✅ WebSocket connected");

		ws.onmessage = (event) => {
			const base64Data = event.data as string;

			// 1️⃣ Convert Base64 into Data URI
			const dataUri = `data:image/jpeg;base64,${base64Data}`;

			// 2️⃣ Update state to render the frame
			setFrameUri(dataUri);
		};

		ws.onclose = () => console.log("❌ WebSocket closed");

		return () => ws.close();
	}, []);

	return (
		<View style={styles.container}>
			<View style={styles.videoWrapper}>
				{frameUri ? (
					<ImageBackground
						source={{ uri: frameUri }}
						style={styles.image}
						resizeMode="cover" // fill the container completely
					>
						<AlertBox />
					</ImageBackground>
				) : (
					<Text>Waiting for video...</Text>
				)}
			</View>
		</View>

	);
}

const styles = StyleSheet.create({
	container: { flex: 1, alignItems: "center", justifyContent: "center" },
	videoWrapper: {
		position: "relative",
		width: 300,
		height: 200,
	},
	image: {
		width: "100%",
		height: "100%",
	},
	alertOverlay: {
		position: "absolute",
		top: 5,
		left: 5,
		backgroundColor: "rgba(255,0,0,0.7)",
		paddingHorizontal: 8,
		paddingVertical: 4,
		borderRadius: 4,
	},
});
