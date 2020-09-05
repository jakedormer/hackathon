product_query = """
  {
    shop {
      name
    }
    products(first: 100) {
      edges {
        node {
          id
          title
          productType
          images(first: 1) {
            edges {
              node {
                altText
                transformedSrc
              }
            }
          }
        }
      }
    }
  }

"""

q_productTypes = """
  {
    shop {
      productTypes (first: 100) {
        edges {
          node
        }
      }
    }
  }

  """