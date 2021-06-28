from xml.dom import minidom

def createNode(doc, parent, tag, value):
	el = doc.createElement(tag)
	
	if type(value) == str:
		el.appendChild(doc.createTextNode(value))
	else:
		el.appendChild(value)

	parent.appendChild(el)
	return el

def createRootNode(doc):
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

def main():
	# --- ROOT ---
	doc = minidom.Document()
	root = createRootNode(doc)
	channelNode = createChannelNode(doc)

	postTitle: str = None
	postCategory: str = ""
	postContent: str = ""

	f = open("input.txt", "r")
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

	# DEBUG
	print(doc.toprettyxml())

	# PRETTY FORMAT
	xmlstr = doc.toprettyxml(indent='\t')
	with open("output_pretty.xml", "w") as f:
		f.write(xmlstr)

	# UTF-8
	# with open("myfile.xml", "w") as xml_file:
	# 	doc.writexml(xml_file, indent='\t', newl='\n', encoding='utf-8')

if __name__ == "__main__":
	main()