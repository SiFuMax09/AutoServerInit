<h1>Server Initialization Script</h1>

<h2>Table of Contents</h2>

<ul>
  <li><a href="#introduction">Introduction</a></li>
  <li><a href="#features">Features</a></li>
  <li><a href="#prerequisites">Prerequisites</a></li>
  <li><a href="#installation">Installation</a></li>
  <li><a href="#usage">Usage</a>
    <ul>
      <li><a href="#command-line-arguments">Command-Line Arguments</a></li>
    </ul>
  </li>
  <li><a href="#examples">Examples</a></li>
  <li><a href="#security-considerations">Security Considerations</a></li>
  <li><a href="#notes-and-best-practices">Notes and Best Practices</a></li>
  <li><a href="#license">License</a></li>
</ul>

<h2 id="introduction">Introduction</h2>

<p>
This script is designed to initialize a server by connecting via SSH and adding SSH public keys to the <code>authorized_keys</code> file. It offers a variety of options to customize the connection and execution, making it ideal for automated server setups and deployments.
</p>

<h2 id="features">Features</h2>

<ul>
  <li><strong>SSH Connection</strong>: Connect to a remote server via SSH using password or key file authentication.</li>
  <li><strong>Add Public Keys</strong>: Adds new SSH public keys to the <code>authorized_keys</code> file without duplicating existing keys.</li>
  <li><strong>Execute Remote Commands</strong>: Option to execute additional commands on the remote server after adding the keys.</li>
  <li><strong>Customizable Connection</strong>: Support for custom SSH ports and connection timeouts.</li>
  <li><strong>Interactive Password Prompt</strong>: Enhanced security by prompting for the password at runtime.</li>
  <li><strong>Dry Run Simulation</strong>: Ability to simulate the script without making actual changes.</li>
  <li><strong>Verbose Mode</strong>: Detailed output during execution for debugging purposes.</li>
  <li><strong>Logging</strong>: Log the script output to a file for audits and troubleshooting.</li>
</ul>

<h2 id="prerequisites">Prerequisites</h2>

<p>Before you can use this script, ensure the following:</p>

<ul>
  <li><strong>Python 3.x</strong> installed on your local system.</li>
  <li>The Python module <strong>paramiko</strong> for SSH connections:</li>
</ul>

<pre><code>pip install paramiko</code></pre>

<h2 id="installation">Installation</h2>

<p>Follow the steps below to install and set up the script:</p>

<ol>
  <li><strong>Download the Script</strong>:
    <ul>
      <li>Save the script as <code>main.py</code> on your local system.</li>
    </ul>
  </li>
  <li><strong>Install Paramiko</strong>:
    <ul>
      <li>Ensure that the <code>paramiko</code> module is installed using the command:</li>
    </ul>
    <pre><code>pip install paramiko</code></pre>
  </li>
  <li><strong>Prepare the <code>pubkeys</code> File</strong>:
    <ul>
      <li>Create a file named <code>pubkeys</code> in the same directory as the script or specify a path using the <code>--pubkeys</code> option.</li>
      <li>Add the SSH public keys you wish to add to the server, <strong>one per line</strong>.</li>
    </ul>
  </li>
  <li><strong>Ensure Correct Permissions</strong>:
    <ul>
      <li>Ensure that the <code>pubkeys</code> file is readable by the user executing the script, and that SSH access to the server is enabled.</li>
    </ul>
  </li>
</ol>

<h2 id="usage">Usage</h2>

<p>Run the script from the command line, providing the necessary arguments. Here’s the basic syntax:</p>

<pre><code>python main.py -ip SERVER_IP -p PASSWORD [OPTIONS]</code></pre>

<h3 id="command-line-arguments">Command-Line Arguments</h3>

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>-h</code>, <code>--help</code></td>
      <td>Show the help message and exit.</td>
    </tr>
    <tr>
      <td><code>-ip IP</code></td>
      <td><strong>(Required)</strong> IP address of the server.</td>
    </tr>
    <tr>
      <td><code>-p PASSWORD</code></td>
      <td>Password for SSH authentication.</td>
    </tr>
    <tr>
      <td><code>--ask-pass</code></td>
      <td>Prompt for password interactively. If specified, you do not need to provide <code>-p</code>.</td>
    </tr>
    <tr>
      <td><code>-u USER</code>, <code>--user USER</code></td>
      <td>Username for SSH authentication (default: <code>root</code>).</td>
    </tr>
    <tr>
      <td><code>--port PORT</code></td>
      <td>SSH port number (default: <code>22</code>).</td>
    </tr>
    <tr>
      <td><code>--pubkeys FILE</code></td>
      <td>Path to the <code>pubkeys</code> file (default: <code>./pubkeys</code>).</td>
    </tr>
    <tr>
      <td><code>-c COMMAND</code>, <code>--command COMMAND</code></td>
      <td>Command to execute on the remote server after adding the keys.</td>
    </tr>
    <tr>
      <td><code>-i FILE</code>, <code>--identity-file FILE</code></td>
      <td>SSH private key file for authentication instead of a password.</td>
    </tr>
    <tr>
      <td><code>-v</code>, <code>--verbose</code></td>
      <td>Enable verbose output during execution.</td>
    </tr>
    <tr>
      <td><code>-t SECONDS</code>, <code>--timeout SECONDS</code></td>
      <td>Timeout for the SSH connection in seconds.</td>
    </tr>
    <tr>
      <td><code>--dry-run</code></td>
      <td>Simulate the script without making any changes.</td>
    </tr>
    <tr>
      <td><code>--log FILE</code></td>
      <td>Path to the log file where the script output will be written.</td>
    </tr>
  </tbody>
</table>

<h2 id="examples">Examples</h2>

<p>Here are some examples to show how the script can be used:</p>

<h3>Connect using password and add keys</h3>
<pre><code>python main.py -ip 192.168.1.100 -p YourPassword</code></pre>

<h3>Using a custom SSH port</h3>
<pre><code>python main.py -ip 192.168.1.100 -p YourPassword --port 2222</code></pre>

<h3>Interactive password prompt</h3>
<pre><code>python main.py -ip 192.168.1.100 --ask-pass</code></pre>

<h3>Authenticate with SSH key file</h3>
<pre><code>python main.py -ip 192.168.1.100 -u username -i ~/.ssh/id_rsa</code></pre>

<h3>Execute an additional command on the server</h3>
<pre><code>python main.py -ip 192.168.1.100 -p YourPassword -c "apt-get update && apt-get install -y nginx"</code></pre>

<h3>Enable verbose mode</h3>
<pre><code>python main.py -ip 192.168.1.100 -p YourPassword --verbose</code></pre>

<h3>Set a connection timeout</h3>
<pre><code>python main.py -ip 192.168.1.100 -p YourPassword --timeout 10</code></pre>

<h3>Simulate the script (dry run)</h3>
<pre><code>python main.py -ip 192.168.1.100 -p YourPassword --dry-run</code></pre>

<h3>Log the output to a file</h3>
<pre><code>python main.py -ip 192.168.1.
