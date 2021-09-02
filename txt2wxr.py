import sys # To Check Python Version
from xml.dom import minidom

def createNode(doc, parent, tag, value):
	"""Create an XML node."""
	el = doc.createElement(tag)
	
	if type(value) == str:
		el.appendChild(doc.createTextNode(value))
	else:
		# Before Python 3.8, there is an issue with minidom.createCDATA
		# Read more: https://bugs.python.org/issue36407
		if not (sys.version_info[0] >= 3 and sys.version_info[1] >= 8):
			value.nodeType = value.TEXT_NODE
		
		el.appendChild(value)

	parent.appendChild(el)
	return el

def createRootNode(doc):
	"""Create an XML Root node."""
	# ---------- ROOT ----------
	root:minidom.Node = doc.createElement("rss")
	root.setAttribute("version", "2.0")
	root.setAttribute("xmlns:excerpt", "http://wordpress.org/export/1.2/excerpt/")
	root.setAttribute("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
	root.setAttribute("xmlns:wfw", "http://wellformedweb.org/CommentAPI/")
	root.setAttribute("xmlns:dc", "http://purl.org/dc/elements/1.1/")
	root.setAttribute("xmlns:wp", "http://wordpress.org/export/1.2/")
	return root

def createChannelNode(doc):
	"""Create an XML node."""
	# ---------- Channel ----------
	channelNode:minidom.Node = doc.createElement("channel")

	# ---------- Channel/wp:wxr_version ----------
	createNode(doc, channelNode, "wp:wxr_version", "1.2")

	# ---------- Channel/wp:author ----------
	wp_authorNode = doc.createElement("wp:author")
	createNode(doc, wp_authorNode, "wp:author_id", "1")
	createNode(doc, wp_authorNode, "wp:author_login", doc.createCDATASection("wordpress"))
	createNode(doc, wp_authorNode, "wp:author_email", doc.createCDATASection("abc@abc.abc"))
	createNode(doc, wp_authorNode, "wp:author_display_name", doc.createCDATASection("wordpress"))
	createNode(doc, wp_authorNode, "wp:author_first_name", doc.createCDATASection(""))
	createNode(doc, wp_authorNode, "wp:author_last_name", doc.createCDATASection(""))
	channelNode.appendChild(wp_authorNode)

	# ---------- Channel/generator ----------
	createNode(doc, channelNode, "generator", "https://wordpress.org/?v=5.7.2")

	return channelNode

def createItemNode(doc, post_title, post_content, post_category):
	"""Create an XML node."""
	# ---------- Channel/item ----------
	itemNode:minidom.Node = doc.createElement('item')
	createNode(doc, itemNode, "title", doc.createCDATASection(post_title))
	createNode(doc, itemNode, "description", "")
	createNode(doc, itemNode, "content:encoded", doc.createCDATASection(post_content))
	createNode(doc, itemNode, "excerpt:encoded", doc.createCDATASection(""))
	createNode(doc, itemNode, "wp:status", doc.createCDATASection("pending"))
	createNode(doc, itemNode, "wp:post_type", doc.createCDATASection("post"))
	temp = createNode(doc, itemNode, "category", doc.createCDATASection(post_category))
	temp.setAttribute("domain", "category")
	temp.setAttribute("nicename", post_category)
	
	return itemNode

def saveToFile(doc, filename):
	"""
	Save an XML document to file

	Params:
	doc: minidom.Document
		XML document
	filename : str
		Path and filename
	"""
	# Before Python 3.8, there is an issue with minidom.createCDATA
	# Read more: https://bugs.python.org/issue36407
	if sys.version_info[0] >= 3 and sys.version_info[1] >= 8:
		xmlstr = doc.toprettyxml(indent='\t')
	else:
		xmlstr = doc.toprettyxml(indent='')

	# Write to file
	with open(filename, "w") as f:
		f.write(xmlstr)

def main():
	# --- ROOT ---
	doc = minidom.Document()
	root = createRootNode(doc)
	channelNode = createChannelNode(doc)

	postTitle: str = None
	postCategory: str = ""
	postContent: str = ""

	f = open("formatted_input.txt", "r")
	# Go line by line to get Post Title, Content, and Category
	for line in f:
		#Case 1: The line is empty, which means End of a Post. Then, create  an item node
		if len(line) == 1:
			itemNode = createItemNode(doc, postTitle, postContent, postCategory)
			channelNode.appendChild(itemNode)
			postContent = str()
		#Case 2: The line starts with @CAT
		elif line.startswith("@CAT:"):
			postCategory = line[5:-1] # Trim the last character '\n'
			postTitle = next(f)[:-1] # Trim the last character '\n'
		#Case 3: Anything else, just concat the lines together.
		else:
			postContent += f"<!-- wp:paragraph -->\n<p>{line[:-1]}</p>\n<!-- /wp:paragraph -->\n"
	else: #End of File
		itemNode = createItemNode(doc, postTitle, postContent, postCategory)
		channelNode.appendChild(itemNode)

	# --- APPEND ---
	root.appendChild(channelNode)
	doc.appendChild(root)

	# Export
	saveToFile(doc, "output.xml")

	# UTF-8
	# with open("myfile.xml", "w") as xml_file:
	# 	doc.writexml(xml_file, indent='\t', newl='\n', encoding='utf-8')

def test():
	# --- ROOT ---
	doc = minidom.Document()
	root = createRootNode(doc)
	channelNode = createChannelNode(doc)
	# createNode(doc, wp_authorNode, "wp:author_login", doc.createCDATASection("wordpress"))

	# --- APPEND ---
	root.appendChild(channelNode)
	doc.appendChild(root)

	# DEBUG
	if sys.version_info[0] >= 3 and sys.version_info[1] >= 8:
		print(doc.toprettyxml())
	else:
		print(doc.toprettyxml(indent=''))

if __name__ == "__main__":
	main()
	# test()