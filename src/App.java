import java.io.File;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.OutputStream;
import com.sun.net.httpserver.HttpServer;
import org.json.JSONObject;

public class App {
    static String scriptDir = "pythonscripts";
    public static void main(String[] args) throws IOException, InterruptedException {

        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);

        // Create a context for the "/chatbot" endpoint
        server.createContext("/chatbot", (exchange -> {
            // Get the message input value from the query parameter
            String message = exchange.getRequestURI().getQuery().split("=")[1];
            try{
                // Generate a response using the message input value
                String responseText = responseToUser(message, 0.8);
                JSONObject response = new JSONObject();
                response.put("response", responseText);
                // Set the response headers
                exchange.getResponseHeaders().set("Content-Type", "text/plain");
                exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
                exchange.getResponseHeaders().add("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
                exchange.getResponseHeaders().add("Access-Control-Allow-Headers", "Content-Type, Authorization");
                exchange.sendResponseHeaders(200, response.toString().getBytes().length);
                OutputStream outputStream = exchange.getResponseBody();
                outputStream.write(response.toString().getBytes());
                outputStream.flush();
                outputStream.close();

            }
            catch (Exception e){
                System.out.println(e);
            }
        }));

    

        // Start the server
        server.start();
    }
    static String chatbotPath = scriptDir + File.separator + "chatbot.py";
    public static String responseToUser(String prompt, double temperature) throws IOException, InterruptedException {
        // Get the directory where the Python script is located
        // Create the process builder
        ProcessBuilder responseToUserBProcessBuilder = new ProcessBuilder("python3", chatbotPath, "response_to_user", prompt, Double.toString(temperature));
        System.out.println(prompt);
        // Redirect the output to a file
        responseToUserBProcessBuilder.redirectOutput(ProcessBuilder.Redirect.to(new File(scriptDir + File.separator + "output.txt")));

        // Start the process
        Process process = responseToUserBProcessBuilder.start();

        // Wait for the process to finish
        int exitCode = process.waitFor();

        // Read the output file
        String response = new String(Files.readAllBytes(Paths.get(scriptDir + File.separator + "output.txt")));

        System.out.println(response);
        // Print the exit code
        System.out.println("Exit code: " + exitCode);

        // Return the response
        return response;
    }
}
