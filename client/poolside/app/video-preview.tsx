import React, { useState, useEffect } from "react";
import { View, Image, StyleSheet, Text } from "react-native";
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
		<>
			<AlertBox></AlertBox>
			<View style={styles.container}>
				{frameUri ? (
					<Image
						source={{ uri: frameUri }}
						style={styles.image}
						resizeMode="contain"
					/>
				) : (
					<Text>Waiting for video...</Text>
				)}
				<Text>Our Video Component</Text>
			</View>
		</>
	);
}

const styles = StyleSheet.create({
	container: { flex: 1, alignItems: "center", justifyContent: "center" },
	image: { width: 300, height: 200 },
});
