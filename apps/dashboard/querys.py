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
          onlineStoreUrl
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


example = """
  {
    shop {
      name
    }
    products(first:100, query:"product_type:coats OR product_type:'T Shirts'") {
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